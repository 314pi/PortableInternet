/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

ChromeUtils.import("resource://gre/modules/XPCOMUtils.jsm");

XPCOMUtils.defineLazyModuleGetter(this, "cal", "resource://calendar/modules/calUtils.jsm", "cal");

/*
 * Data structures and algorithms used within the codebase
 */

// NOTE: This module should not be loaded directly, it is available when
// including calUtils.jsm under the cal.data namespace.

this.EXPORTED_SYMBOLS = ["caldata"]; /* exported caldata */

class PropertyMap extends Map {
    get simpleEnumerator() {
        let entries = [...this.entries()].filter(([key, value]) => value !== undefined);
        let index = 0;

        return {
            QueryInterface: XPCOMUtils.generateQI([Components.interfaces.nsISimpleEnumerator]),

            hasMoreElements: function() {
                return index < entries.length;
            },

            getNext: function() {
                if (!this.hasMoreElements()) {
                    throw Components.results.NS_ERROR_UNEXPECTED;
                }

                let [name, value] = entries[index++];
                return {
                    QueryInterface: XPCOMUtils.generateQI([Components.interfaces.nsIProperty]),
                    name: name,
                    value: value
                };
            }
        };
    }
}

class ListenerSet extends Set {
    constructor(iid, iterable) {
        super(iterable);
        this.mIID = iid;
    }

    add(item) {
        super.add(item.QueryInterface(this.mIID));
    }

    has(item) {
        return super.has(item.QueryInterface(this.mIID));
    }

    delete(item) {
        super.delete(item.QueryInterface(this.mIID));
    }

    notify(func, args=[]) {
        let currentObservers = [...this.values()];
        for (let observer of currentObservers) {
            try {
                observer[func](...args);
            } catch (exc) {
                let stack = exc.stack || (exc.location ? exc.location.formattedStack : null);
                Components.utils.reportError(exc + "\nSTACK: " + stack);
            }
        }
    }
}

class ObserverSet extends ListenerSet {
    constructor(iid, iterable) {
        super(iid, iterable);
        this.mBatchCount = 0;
    }

    get batchCount() {
        return this.mBatchCount;
    }

    notify(func, args=[]) {
        switch (func) {
            case "onStartBatch":
                ++this.mBatchCount;
                break;
            case "onEndBatch":
                --this.mBatchCount;
                break;
        }
        return super.notify(func, args);
    }

    add(item) {
        if (!this.has(item) && this.mBatchCount > 0) {
            // Replay batch notifications, because the onEndBatch notifications are yet to come.
            // We may think about doing the reverse on remove, though I currently see no need:
            for (let i = this.mBatchCount; i; i--) {
                item.onStartBatch();
            }
        }
        super.add(item);
    }
}

/**
 * This object implements calIOperation and could group multiple sub
 * operations into one. You can pass a cancel function which is called once
 * the operation group is cancelled.
 * Users must call notifyCompleted() once all sub operations have been
 * successful, else the operation group will stay pending.
 * The reason for the latter is that providers currently should (but need
 * not) implement (and return) calIOperation handles, thus there may be pending
 * calendar operations (without handle).
 */
class OperationGroup {
    static nextGroupId() {
        if (typeof OperationGroup.mOpGroupId == "undefined") {
            OperationGroup.mOpGroupId = 0;
        }

        return OperationGroup.mOpGroupId++;
    }

    constructor(aCancelFunc) {
        this.mId = cal.getUUID() + "-" + OperationGroup.nextGroupId();
        this.mIsPending = true;

        this.mCancelFunc = aCancelFunc;
        this.mSubOperations = [];
        this.mStatus = Components.results.NS_OK;
    }

    get id() { return this.mId; }
    get isPending() { return this.mIsPending; }
    get status() { return this.mStatus; }
    get isEmpty() { return this.mSubOperations.length == 0; }

    add(aOperation) {
        if (aOperation && aOperation.isPending) {
            this.mSubOperations.push(aOperation);
        }
    }

    remove(aOperation) {
        if (aOperation) {
            this.mSubOperations = this.mSubOperations.filter(operation => aOperation.id != operation.id);
        }
    }

    notifyCompleted(aStatus) {
        cal.ASSERT(this.isPending, "[OperationGroup_notifyCompleted] this.isPending");
        if (this.isPending) {
            this.mIsPending = false;
            if (aStatus) {
                this.mStatus = aStatus;
            }
        }
    }

    cancel(aStatus=Components.interfaces.calIErrors.OPERATION_CANCELLED) {
        if (this.isPending) {
            this.notifyCompleted(aStatus);
            let cancelFunc = this.mCancelFunc;
            if (cancelFunc) {
                this.mCancelFunc = null;
                cancelFunc();
            }
            let subOperations = this.mSubOperations;
            this.mSubOperations = [];
            for (let operation of subOperations) {
                operation.cancel(Components.interfaces.calIErrors.OPERATION_CANCELLED);
            }
        }
    }

    toString() {
        return `[OperationGroup id=${this.id}]`;
    }
}

var caldata = {
    ListenerSet: ListenerSet,
    ObserverSet: ObserverSet,
    PropertyMap: PropertyMap,
    OperationGroup: OperationGroup,

    /**
     * Use the binary search algorithm to search for an item in an array.
     * function.
     *
     * The comptor function may look as follows for calIDateTime objects.
     *     function comptor(a, b) {
     *         return a.compare(b);
     *     }
     * If no comptor is specified, the default greater-than comptor will be used.
     *
     * @param itemArray             The array to search.
     * @param newItem               The item to search in the array.
     * @param comptor               A comparation function that can compare two items.
     * @return                      The index of the new item.
     */
    binarySearch: function(itemArray, newItem, comptor) {
        function binarySearchInternal(low, high) {
            // Are we done yet?
            if (low == high) {
                return low + (comptor(newItem, itemArray[low]) < 0 ? 0 : 1);
            }

            let mid = Math.floor(low + ((high - low) / 2));
            let cmp = comptor(newItem, itemArray[mid]);
            if (cmp > 0) {
                return binarySearchInternal(mid + 1, high);
            } else if (cmp < 0) {
                return binarySearchInternal(low, mid);
            } else {
                return mid;
            }
        }

        if (itemArray.length < 1) {
            return -1;
        }
        if (!comptor) {
            comptor = function(a, b) {
                return (a > b) - (a < b);
            };
        }
        return binarySearchInternal(0, itemArray.length - 1);
    },

    /**
     * Insert a new node underneath the given parentNode, using binary search. See binarySearch
     * for a note on how the comptor works.
     *
     * @param parentNode           The parent node underneath the new node should be inserted.
     * @param inserNode            The node to insert
     * @param aItem                The calendar item to add a widget for.
     * @param comptor              A comparison function that can compare two items (not DOM Nodes!)
     * @param discardDuplicates    Use the comptor function to check if the item in
     *                               question is already in the array. If so, the
     *                               new item is not inserted.
     * @param itemAccessor         [optional] A function that receives a DOM node and returns the associated item
     *                               If null, this function will be used: function(n) n.item
     */
    binaryInsertNode: function(parentNode, insertNode, aItem, comptor, discardDuplicates, itemAccessor) {
        let accessor = itemAccessor || caldata.binaryInsertNodeDefaultAccessor;

        // Get the index of the node before which the inserNode will be inserted
        let newIndex = caldata.binarySearch(Array.from(parentNode.childNodes, accessor), aItem, comptor);

        if (newIndex < 0) {
            parentNode.appendChild(insertNode);
            newIndex = 0;
        } else if (!discardDuplicates ||
            comptor(accessor(parentNode.childNodes[Math.min(newIndex, parentNode.childNodes.length - 1)]), aItem) >= 0) {
            // Only add the node if duplicates should not be discarded, or if
            // they should and the childNode[newIndex] == node.
            let node = parentNode.childNodes[newIndex];
            parentNode.insertBefore(insertNode, node);
        }
        return newIndex;
    },
    binaryInsertNodeDefaultAccessor: n => n.item,

    /**
     * Insert an item into the given array, using binary search. See binarySearch
     * for a note on how the comptor works.
     *
     * @param itemArray             The array to insert into.
     * @param item                  The item to insert into the array.
     * @param comptor               A comparation function that can compare two items.
     * @param discardDuplicates     Use the comptor function to check if the item in
     *                                question is already in the array. If so, the
     *                                new item is not inserted.
     * @return                      The index of the new item.
     */
    binaryInsert: function(itemArray, item, comptor, discardDuplicates) {
        let newIndex = caldata.binarySearch(itemArray, item, comptor);

        if (newIndex < 0) {
            itemArray.push(item);
            newIndex = 0;
        } else if (!discardDuplicates ||
                    comptor(itemArray[Math.min(newIndex, itemArray.length - 1)], item) != 0) {
            // Only add the item if duplicates should not be discarded, or if
            // they should and itemArray[newIndex] != item.
            itemArray.splice(newIndex, 0, item);
        }
        return newIndex;
    },

    /**
     * Generic object comparer
     * Use to compare two objects which are not of type calIItemBase, in order
     * to avoid the js-wrapping issues mentioned above.
     *
     * @param aObject        first object to be compared
     * @param aOtherObject   second object to be compared
     * @param aIID           IID to use in comparison, undefined/null defaults to nsISupports
     */
    compareObjects: function(aObject, aOtherObject, aIID) {
        // xxx todo: seems to work fine e.g. for WCAP, but I still mistrust this trickery...
        //           Anybody knows an official API that could be used for this purpose?
        //           For what reason do clients need to pass aIID since
        //           every XPCOM object has to implement nsISupports?
        //           XPCOM (like COM, like UNO, ...) defines that QueryInterface *only* needs to return
        //           the very same pointer for nsISupports during its lifetime.
        if (!aIID) {
            aIID = Components.interfaces.nsISupports;
        }
        let sip1 = Components.classes["@mozilla.org/supports-interface-pointer;1"]
                             .createInstance(Components.interfaces.nsISupportsInterfacePointer);
        sip1.data = aObject;
        sip1.dataIID = aIID;

        let sip2 = Components.classes["@mozilla.org/supports-interface-pointer;1"]
                             .createInstance(Components.interfaces.nsISupportsInterfacePointer);
        sip2.data = aOtherObject;
        sip2.dataIID = aIID;
        return sip1.data == sip2.data;
    }
};
