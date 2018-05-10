/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

ChromeUtils.import("resource://gre/modules/Deprecated.jsm");
ChromeUtils.import("resource://gre/modules/Preferences.jsm");
ChromeUtils.import("resource://gre/modules/Services.jsm");
ChromeUtils.import("resource://gre/modules/XPCOMUtils.jsm");

ChromeUtils.import("resource://calendar/modules/calHashedArray.jsm");

XPCOMUtils.defineLazyModuleGetter(this, "cal", "resource://calendar/modules/calUtils.jsm", "cal");

/*
 * Calendar item related functions
 */

// NOTE: This module should not be loaded directly, it is available when
// including calUtils.jsm under the cal.item namespace.

this.EXPORTED_SYMBOLS = ["calitem", "itemDiff"]; /* exported calitem, itemDiff */

var calitem = {
    ItemDiff: (function() {
        /**
         * Given two sets of items, find out which items were added, changed or
         * removed.
         *
         * The general flow is to first use load/load1 methods to load the engine with
         * the first set of items, then use difference/difference1 to load the set of
         * items to diff against. Afterwards, call the complete method to tell the
         * engine that no more items are coming.
         *
         * You can then access the mAddedItems/mModifiedItems/mDeletedItems attributes to
         * get the items that were changed during the process.
         */
        function ItemDiff() {
            this.reset();
        }

        ItemDiff.prototype = {
            STATE_INITIAL: 1,
            STATE_LOADING: 2,
            STATE_DIFFERING: 4,
            STATE_COMPLETED: 8,

            state: 1,
            mInitialItems: null,

            mModifiedItems: null,
            mModifiedOldItems: null,
            mAddedItems: null,
            mDeletedItems: null,

            /**
             * Expect the difference engine to be in the given state.
             *
             * @param aState    The state to be in
             * @param aMethod   The method name expecting the state
             */
            _expectState: function(aState, aMethod) {
                if ((this.state & aState) == 0) {
                    throw new Error("ItemDiff method " + aMethod +
                                    " called while in unexpected state " + this.state);
                }
            },

            /**
             * Load the difference engine with one item, see load.
             *
             * @param item      The item to load
             */
            load1: function(item) {
                this.load([item]);
            },

            /**
             * Loads an array of items. This step cannot be executed
             * after calling the difference methods.
             *
             * @param items     The array of items to load
             */
            load: function(items) {
                this._expectState(this.STATE_INITIAL | this.STATE_LOADING, "load");

                for (let item of items) {
                    this.mInitialItems[item.hashId] = item;
                }

                this.state = this.STATE_LOADING;
            },

            /**
             * Calculates the difference for the passed item, see difference.
             *
             * @param item      The item to calculate difference with
             */
            difference1: function(item) {
                this.difference([item]);
            },

            /**
             * Calculate the difference for the array of items. This method should be
             * called after all load methods and before the complete method.
             *
             * @param items     The array of items to calculate difference with
             */
            difference: function(items) {
                this._expectState(this.STATE_INITIAL | this.STATE_LOADING | this.STATE_DIFFERING, "difference");

                this.mModifiedOldItems.startBatch();
                this.mModifiedItems.startBatch();
                this.mAddedItems.startBatch();

                for (let item of items) {
                    if (item.hashId in this.mInitialItems) {
                        let oldItem = this.mInitialItems[item.hashId];
                        this.mModifiedOldItems.addItem(oldItem);
                        this.mModifiedItems.addItem(item);
                    } else {
                        this.mAddedItems.addItem(item);
                    }
                    delete this.mInitialItems[item.hashId];
                }

                this.mModifiedOldItems.endBatch();
                this.mModifiedItems.endBatch();
                this.mAddedItems.endBatch();

                this.state = this.STATE_DIFFERING;
            },

            /**
             * Tell the engine that all load and difference calls have been made, this
             * makes sure that all item states are correctly returned.
             */
            complete: function() {
                this._expectState(this.STATE_INITIAL | this.STATE_LOADING | this.STATE_DIFFERING, "complete");

                this.mDeletedItems.startBatch();

                for (let hashId in this.mInitialItems) {
                    let item = this.mInitialItems[hashId];
                    this.mDeletedItems.addItem(item);
                }

                this.mDeletedItems.endBatch();
                this.mInitialItems = {};

                this.state = this.STATE_COMPLETED;
            },

            /** @return a HashedArray containing the new version of the modified items */
            get modifiedItems() {
                this._expectState(this.STATE_COMPLETED, "get modifiedItems");
                return this.mModifiedItems;
            },

            /** @return a HashedArray containing the old version of the modified items */
            get modifiedOldItems() {
                this._expectState(this.STATE_COMPLETED, "get modifiedOldItems");
                return this.mModifiedOldItems;
            },

            /** @return a HashedArray containing added items */
            get addedItems() {
                this._expectState(this.STATE_COMPLETED, "get addedItems");
                return this.mAddedItems;
            },

            /** @return a HashedArray containing deleted items */
            get deletedItems() {
                this._expectState(this.STATE_COMPLETED, "get deletedItems");
                return this.mDeletedItems;
            },

            /** @return the number of loaded items */
            get count() {
                return Object.keys(this.mInitialItems).length;
            },

            /**
             * Resets the difference engine to its initial state.
             */
            reset: function() {
                this.mInitialItems = {};
                this.mModifiedItems = new cal.HashedArray();
                this.mModifiedOldItems = new cal.HashedArray();
                this.mAddedItems = new cal.HashedArray();
                this.mDeletedItems = new cal.HashedArray();
                this.state = this.STATE_INITIAL;
            }
        };
        return ItemDiff;
    })(),

    /**
     * Checks if an item is supported by a Calendar.
     *
     * @param aCalendar the calendar
     * @param aItem the item either a task or an event
     * @return true or false
     */
    isItemSupported: function(aItem, aCalendar) {
        if (calitem.isToDo(aItem)) {
            return aCalendar.getProperty("capabilities.tasks.supported") !== false;
        } else if (calitem.isEvent(aItem)) {
            return aCalendar.getProperty("capabilities.events.supported") !== false;
        }
        return false;
    },

    /*
     * Checks whether a calendar supports events
     *
     * @param aCalendar
     */
    isEventCalendar: function(aCalendar) {
        return aCalendar.getProperty("capabilities.events.supported") !== false;
    },

    /*
     * Checks whether a calendar supports tasks
     *
     * @param aCalendar
     */
    isTaskCalendar: function(aCalendar) {
        return aCalendar.getProperty("capabilities.tasks.supported") !== false;
    },


    /**
     * Determines whether or not the aObject is a calIEvent
     *
     * @param aObject  the object to test
     * @returns        true if the object is a calIEvent, false otherwise
     */
    isEvent: function(aObject) {
        return cal.wrapInstance(aObject, Components.interfaces.calIEvent) != null;
    },

    /**
     * Determines whether or not the aObject is a calITodo
     *
     * @param aObject  the object to test
     * @returns        true if the object is a calITodo, false otherwise
     */
    isToDo: function(aObject) {
        return cal.wrapInstance(aObject, Components.interfaces.calITodo) != null;
    },

    /**
     * Checks whether the passed item fits into the demanded range.
     *
     * @param item               the item
     * @param rangeStart         (inclusive) range start or null (open range)
     * @param rangeStart         (exclusive) range end or null (open range)
     * @param returnDtstartOrDue returns item's start (or due) date in case
     *                           the item is in the specified Range; null otherwise.
     */
    checkIfInRange: function(item, rangeStart, rangeEnd, returnDtstartOrDue) {
        let startDate;
        let endDate;
        let queryStart = cal.dtz.ensureDateTime(rangeStart);
        if (calitem.isEvent(item)) {
            startDate = item.startDate;
            if (!startDate) { // DTSTART mandatory
                // xxx todo: should we assert this case?
                return null;
            }
            endDate = item.endDate || startDate;
        } else {
            let dueDate = item.dueDate;
            startDate = item.entryDate || dueDate;
            if (!item.entryDate) {
                if (returnDtstartOrDue) { // DTSTART or DUE mandatory
                    return null;
                }
                // 3.6.2. To-do Component
                // A "VTODO" calendar component without the "DTSTART" and "DUE" (or
                // "DURATION") properties specifies a to-do that will be associated
                // with each successive calendar date, until it is completed.
                let completedDate = cal.dtz.ensureDateTime(item.completedDate);
                dueDate = cal.dtz.ensureDateTime(dueDate);
                return !completedDate || !queryStart ||
                       completedDate.compare(queryStart) > 0 ||
                       (dueDate && dueDate.compare(queryStart) >= 0);
            }
            endDate = dueDate || startDate;
        }

        let start = cal.dtz.ensureDateTime(startDate);
        let end = cal.dtz.ensureDateTime(endDate);
        let queryEnd = cal.dtz.ensureDateTime(rangeEnd);

        if (start.compare(end) == 0) {
            if ((!queryStart || start.compare(queryStart) >= 0) &&
                (!queryEnd || start.compare(queryEnd) < 0)) {
                return startDate;
            }
        } else if ((!queryEnd || start.compare(queryEnd) < 0) &&
                   (!queryStart || end.compare(queryStart) > 0)) {
            return startDate;
        }
        return null;
    },

    setItemProperty: function(item, propertyName, aValue, aCapability) {
        let isSupported = item.calendar.getProperty("capabilities." + aCapability + ".supported") !== false;
        let value = aCapability && !isSupported ? null : aValue;

        switch (propertyName) {
            case "startDate":
                if ((value.isDate && !item.startDate.isDate) ||
                    (!value.isDate && item.startDate.isDate) ||
                    !cal.data.compareObjects(value.timezone, item.startDate.timezone) ||
                    value.compare(item.startDate) != 0) {
                    item.startDate = value;
                }
                break;
            case "endDate":
                if ((value.isDate && !item.endDate.isDate) ||
                    (!value.isDate && item.endDate.isDate) ||
                    !cal.data.compareObjects(value.timezone, item.endDate.timezone) ||
                    value.compare(item.endDate) != 0) {
                    item.endDate = value;
                }
                break;
            case "entryDate":
                if (value == item.entryDate) {
                    break;
                }
                if ((value && !item.entryDate) ||
                    (!value && item.entryDate) ||
                    value.isDate != item.entryDate.isDate ||
                    !cal.data.compareObjects(value.timezone, item.entryDate.timezone) ||
                    value.compare(item.entryDate) != 0) {
                    item.entryDate = value;
                }
                break;
            case "dueDate":
                if (value == item.dueDate) {
                    break;
                }
                if ((value && !item.dueDate) ||
                    (!value && item.dueDate) ||
                    value.isDate != item.dueDate.isDate ||
                    !cal.data.compareObjects(value.timezone, item.dueDate.timezone) ||
                    value.compare(item.dueDate) != 0) {
                    item.dueDate = value;
                }
                break;
            case "isCompleted":
                if (value != item.isCompleted) {
                    item.isCompleted = value;
                }
                break;
            case "PERCENT-COMPLETE": {
                let perc = parseInt(item.getProperty(propertyName), 10);
                if (isNaN(perc)) {
                    perc = 0;
                }
                if (perc != value) {
                    item.setProperty(propertyName, value);
                }
                break;
            }
            case "title":
                if (value != item.title) {
                    item.title = value;
                }
                break;
            default:
                if (!value || value == "") {
                    item.deleteProperty(propertyName);
                } else if (item.getProperty(propertyName) != value) {
                    item.setProperty(propertyName, value);
                }
                break;
        }
    },

    /**
     * Returns the default transparency to apply for an event depending on whether its an all-day event
     *
     * @param aIsAllDay      If true, the default transparency for all-day events is returned
     */
    getEventDefaultTransparency: function(aIsAllDay) {
        let transp = null;
        if (aIsAllDay) {
            transp = Preferences.get("calendar.events.defaultTransparency.allday.transparent", false)
                     ? "TRANSPARENT"
                     : "OPAQUE";
        } else {
            transp = Preferences.get("calendar.events.defaultTransparency.standard.transparent", false)
                     ? "TRANSPARENT"
                     : "OPAQUE";
        }
        return transp;
    },


    /**
     * Compare two items by *content*, leaving out any revision information such as
     * X-MOZ-GENERATION, SEQUENCE, DTSTAMP, LAST-MODIFIED.

     * The format for the parameters to ignore object is:
     * { "PROPERTY-NAME": ["PARAM-NAME", ...] }
     *
     * If aIgnoreProps is not passed, these properties are ignored:
     *  X-MOZ-GENERATION, SEQUENCE, DTSTAMP, LAST-MODIFIED, X-MOZ-SEND-INVITATIONS
     *
     * If aIgnoreParams is not passed, these parameters are ignored:
     *  ATTENDEE: CN
     *  ORGANIZER: CN
     *
     * @param aFirstItem        The item to compare.
     * @param aSecondItem       The item to compare to.
     * @param aIgnoreProps      (optional) An array of parameters to ignore.
     * @param aIgnoreParams     (optional) An object describing which parameters to
     *                                     ignore.
     * @return                  True, if items match.
     */
    compareContent: function(aFirstItem, aSecondItem, aIgnoreProps, aIgnoreParams) {
        let ignoreProps = arr2hash(aIgnoreProps || [
            "SEQUENCE", "DTSTAMP", "LAST-MODIFIED", "X-MOZ-GENERATION", "X-MICROSOFT-DISALLOW-COUNTER",
            "X-MOZ-SEND-INVITATIONS", "X-MOZ-SEND-INVITATIONS-UNDISCLOSED"
        ]);

        let ignoreParams = aIgnoreParams ||
            { ATTENDEE: ["CN"], ORGANIZER: ["CN"] };
        for (let x in ignoreParams) {
            ignoreParams[x] = arr2hash(ignoreParams[x]);
        }

        function arr2hash(arr) {
            let hash = {};
            for (let x of arr) {
                hash[x] = true;
            }
            return hash;
        }

        // This doesn't have to be super correct rfc5545, it just needs to be
        // in the same order
        function normalizeComponent(comp) {
            let props = [];
            for (let prop of cal.iterate.icalProperty(comp)) {
                if (!(prop.propertyName in ignoreProps)) {
                    props.push(normalizeProperty(prop));
                }
            }
            props = props.sort();

            let comps = [];
            for (let subcomp of cal.iterate.icalSubcomponent(comp)) {
                comps.push(normalizeComponent(subcomp));
            }
            comps = comps.sort();

            return comp.componentType + props.join("\r\n") + comps.join("\r\n");
        }

        function normalizeProperty(prop) {
            let params = [...cal.iterate.icalParameter(prop)]
                .filter(([k, v]) => !(prop.propertyName in ignoreParams) ||
                       !(k in ignoreParams[prop.propertyName]))
                .map(([k, v]) => k + "=" + v)
                .sort();

            return prop.propertyName + ";" +
                   params.join(";") + ":" +
                   prop.valueAsIcalString;
        }

        return normalizeComponent(aFirstItem.icalComponent) ==
               normalizeComponent(aSecondItem.icalComponent);
    },

    /**
     * Shifts an item by the given timely offset.
     *
     * @param item an item
     * @param offset an offset (calIDuration)
     */
    shiftOffset: function(item, offset) {
        // When modifying dates explicitly using the setters is important
        // since those may triggers e.g. calIRecurrenceInfo::onStartDateChange
        // or invalidate other properties. Moreover don't modify the date-time objects
        // without cloning, because changes cannot be calculated if doing so.
        if (calitem.isEvent(item)) {
            let date = item.startDate.clone();
            date.addDuration(offset);
            item.startDate = date;
            date = item.endDate.clone();
            date.addDuration(offset);
            item.endDate = date;
        } else /* isToDo */ {
            if (item.entryDate) {
                let date = item.entryDate.clone();
                date.addDuration(offset);
                item.entryDate = date;
            }
            if (item.dueDate) {
                let date = item.dueDate.clone();
                date.addDuration(offset);
                item.dueDate = date;
            }
        }
    },

    /**
     * moves an item to another startDate
     *
     * @param aOldItem             The Item to be modified
     * @param aNewDate             The date at which the new item is going to start
     * @return                     The modified item
     */
    moveToDate: function(aOldItem, aNewDate) {
        let newItem = aOldItem.clone();
        let start = (aOldItem[cal.dtz.startDateProp(aOldItem)] ||
                     aOldItem[cal.dtz.endDateProp(aOldItem)]).clone();
        let isDate = start.isDate;
        start.resetTo(aNewDate.year, aNewDate.month, aNewDate.day,
                      start.hour, start.minute, start.second,
                      start.timezone);
        start.isDate = isDate;
        if (newItem[cal.dtz.startDateProp(newItem)]) {
            newItem[cal.dtz.startDateProp(newItem)] = start;
            let oldDuration = aOldItem.duration;
            if (oldDuration) {
                let oldEnd = aOldItem[cal.dtz.endDateProp(aOldItem)];
                let newEnd = start.clone();
                newEnd.addDuration(oldDuration);
                newEnd = newEnd.getInTimezone(oldEnd.timezone);
                newItem[cal.dtz.endDateProp(newItem)] = newEnd;
            }
        } else if (newItem[cal.dtz.endDateProp(newItem)]) {
            newItem[cal.dtz.endDateProp(newItem)] = start;
        }
        return newItem;
    },

    /**
     * Shortcut function to serialize an item (including all overridden items).
     */
    serialize: function(aItem) {
        let serializer = Components.classes["@mozilla.org/calendar/ics-serializer;1"]
                                   .createInstance(Components.interfaces.calIIcsSerializer);
        serializer.addItems([aItem], 1);
        return serializer.serializeToString();
    },

    /**
     * Centralized funtions for accessing prodid and version
     */
    get productId() { return "-//Mozilla.org/NONSGML Mozilla Calendar V1.1//EN"; },
    get productVersion() { return "2.0"; },

    /**
     * This is a centralized function for setting the prodid and version on an
     * ical component.  This should be used whenever you need to set the prodid
     * and version on a calIcalComponent object.
     *
     * @param aIcalComponent        The ical component to set the prodid and
     *                                version on.
     */
    setStaticProps: function(aIcalComponent) {
        // Throw for an invalid parameter
        aIcalComponent = cal.wrapInstance(aIcalComponent, Components.interfaces.calIIcalComponent);
        if (!aIcalComponent) {
            throw Components.results.NS_ERROR_INVALID_ARG;
        }
        // Set the prodid and version
        aIcalComponent.prodid = calitem.productId;
        aIcalComponent.version = calitem.productVersion;
    },

    /**
     * Search for already open item dialog.
     *
     * @param aItem     The item of the dialog to search for.
     */
    findWindow: function(aItem) {
        // check for existing dialog windows
        let list = Services.wm.getEnumerator("Calendar:EventDialog");
        while (list.hasMoreElements()) {
            let dlg = list.getNext();
            if (dlg.arguments[0] &&
                dlg.arguments[0].mode == "modify" &&
                dlg.arguments[0].calendarEvent &&
                dlg.arguments[0].calendarEvent.hashId == aItem.hashId) {
                return dlg;
            }
        }
        // check for existing summary windows
        list = Services.wm.getEnumerator("Calendar:EventSummaryDialog");
        while (list.hasMoreElements()) {
            let dlg = list.getNext();
            if (dlg.calendarItem &&
                dlg.calendarItem.hashId == aItem.hashId) {
                return dlg;
            }
        }
        return null;
    },

    /**
     * sets the 'isDate' property of an item
     *
     * @param aItem         The Item to be modified
     * @param aIsDate       True or false indicating the new value of 'isDate'
     * @return              The modified item
     */
    setToAllDay: function(aItem, aIsDate) {
        let start = aItem[cal.dtz.startDateProp(aItem)];
        let end = aItem[cal.dtz.endDateProp(aItem)];
        if (start || end) {
            let item = aItem.clone();
            if (start && (start.isDate != aIsDate)) {
                start = start.clone();
                start.isDate = aIsDate;
                item[cal.dtz.startDateProp(item)] = start;
            }
            if (end && (end.isDate != aIsDate)) {
                end = end.clone();
                end.isDate = aIsDate;
                item[cal.dtz.endDateProp(item)] = end;
            }
            return item;
        } else {
            return aItem;
        }
    },

    /**
     * This function return the progress state of a task:
     * completed, overdue, duetoday, inprogress, future
     *
     * @param aTask     The task to check.
     * @return          The progress atom.
     */
    getProgressAtom: function(aTask) {
        let nowdate = new Date();

        if (aTask.recurrenceInfo) {
            return "repeating";
        }

        if (aTask.isCompleted) {
            return "completed";
        }

        if (aTask.dueDate && aTask.dueDate.isValid) {
            if (cal.dtz.dateTimeToJsDate(aTask.dueDate).getTime() < nowdate.getTime()) {
                return "overdue";
            } else if (aTask.dueDate.year == nowdate.getFullYear() &&
                       aTask.dueDate.month == nowdate.getMonth() &&
                       aTask.dueDate.day == nowdate.getDate()) {
                return "duetoday";
            }
        }

        if (aTask.entryDate && aTask.entryDate.isValid &&
            cal.dtz.dateTimeToJsDate(aTask.entryDate).getTime() < nowdate.getTime()) {
            return "inprogress";
        }

        return "future";
    }
};

// Backwards compatibility for bug 905097. Please remove with Thunderbird 61.
class itemDiff extends calitem.ItemDiff {
    constructor(...args) {
        super(...args);
        Deprecated.warning("calItemUtils' itemDiff has changed to calUtils' cal.item.ItemDiff",
                           "https://bugzilla.mozilla.org/show_bug.cgi?id=905097",
                           Components.stack.caller);
    }
}
