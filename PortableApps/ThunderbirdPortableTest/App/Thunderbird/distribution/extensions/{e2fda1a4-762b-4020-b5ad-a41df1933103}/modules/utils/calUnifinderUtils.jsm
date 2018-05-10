/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

ChromeUtils.import("resource:///modules/mailServices.js");
ChromeUtils.import("resource://gre/modules/XPCOMUtils.jsm");

XPCOMUtils.defineLazyModuleGetter(this, "cal", "resource://calendar/modules/calUtils.jsm", "cal");

/*
 * Helpers for the unifinder
 */

// NOTE: This module should not be loaded directly, it is available when
// including calUtils.jsm under the cal.unifinder namespace.

this.EXPORTED_SYMBOLS = ["calunifinder"]; /* exported calunifinder */

var calunifinder = {
    /**
     * Retrieves the value that is used for comparison for the item with the given
     * property.
     *
     * @param {calIItemBaes} aItem      The item to retrieve the sort key for
     * @param {String} aKey             The property name that should be sorted
     * @return {*}                      The value used in sort comparison
     */
    getItemSortKey: function(aItem, aKey) {
        const taskStatus = ["NEEDS-ACTION", "IN-PROCESS", "COMPLETED", "CANCELLED"];
        const eventStatus = ["TENTATIVE", "CONFIRMED", "CANCELLED"];

        switch (aKey) {
            case "priority":
                return aItem.priority || 5;

            case "title":
                return aItem.title || "";

            case "entryDate":
            case "startDate":
            case "dueDate":
            case "endDate":
            case "completedDate":
                if (aItem[aKey] == null) {
                    return -62168601600000000; // ns value for (0000/00/00 00:00:00)
                }
                return aItem[aKey].nativeTime;

            case "percentComplete":
                return aItem.percentComplete;

            case "categories":
                return aItem.getCategories({}).join(", ");

            case "location":
                return aItem.getProperty("LOCATION") || "";

            case "status": {
                let statusSet = cal.item.isEvent(aItem) ? eventStatus : taskStatus;
                return statusSet.indexOf(aItem.status);
            }
            case "calendar":
                return aItem.calendar.name || "";

            default:
                return null;
        }
    },

    /**
     * Returns a sort function for the given sort type.
     *
     * @param {String} aSortKey             The sort key to get the compare function for
     * @return {Function}                   The function to be used for sorting values of the type
     */
    sortEntryComparer: function(aSortKey) {
        switch (aSortKey) {
            case "title":
            case "categories":
            case "location":
            case "calendar":
                return sortCompare.string;

            // All dates use "date_filled"
            case "completedDate":
            case "startDate":
            case "endDate":
            case "dueDate":
            case "entryDate":
                return sortCompare.date_filled;

            case "priority":
            case "percentComplete":
            case "status":
                return sortCompare.number;
            default:
                return sortCompare.unknown;
        }
    },

    /**
     * Sort the unifinder items by the given sort key, using the modifier to flip direction. The
     * items are sorted in place.
     *
     * @param {calIItemBase[]} aItems           The items to sort
     * @param {String} aSortKey                 The item sort key
     * @param {?Number} aModifier               Either 1 or -1, to indicate sort direction
     */
    sortItems: function(aItems, aSortKey, aModifier=1) {
        let comparer = calunifinder.sortEntryComparer(aSortKey);
        aItems.sort((a, b) => {
            let sortvalA = calunifinder.getItemSortKey(a, aSortKey);
            let sortvalB = calunifinder.getItemSortKey(b, aSortKey);
            return comparer(sortvalA, sortvalB, aModifier);
        });
    }
};

/**
 * Sort compare functions that can be used with Array sort(). The modifier can flip the sort
 * direction by passing -1 or 1.
 */
const sortCompare = calunifinder.sortEntryComparer._sortCompare = {
    /**
     * Compare two things as if they were numbers.
     *
     * @param {*} a                 The first thing to compare
     * @param {*} b                 The second thing to compare
     * @param {Number} modifier     -1 to flip direction, or 1
     * @return {Number}             Either -1, 0, or 1
     */
    number: function(a, b, modifier=1) {
        return sortCompare.general(Number(a), Number(b), modifier);
    },

    /**
     * Compare two things as if they were dates.
     *
     * @param {*} a                 The first thing to compare
     * @param {*} b                 The second thing to compare
     * @param {Number} modifier     -1 to flip direction, or 1
     * @return {Number}             Either -1, 0, or 1
     */
    date: function(a, b, modifier=1) {
        return sortCompare.general(a, b, modifier);
    },

    /**
     * Compare two things generally, using the typical ((a > b) - (a < b))
     *
     * @param {*} a                 The first thing to compare
     * @param {*} b                 The second thing to compare
     * @param {Number} modifier     -1 to flip direction, or 1
     * @return {Number}             Either -1, 0, or 1
     */
    general: function(a, b, modifier=1) {
        return ((a > b) - (a < b)) * modifier;
    },

    /**
     * Compare two dates, keeping the nativeTime zero date in mind.
     *
     * @param {*} a                 The first date to compare
     * @param {*} b                 The second date to compare
     * @param {Number} modifier     -1 to flip direction, or 1
     * @return {Number}             Either -1, 0, or 1
     */
    date_filled: function(a, b, modifier=1) {
        const NULL_DATE = -62168601600000000;

        if (a == b) {
            return 0;
        } else if (a == NULL_DATE) {
            return 1;
        } else if (b == NULL_DATE) {
            return -1;
        } else {
            return sortCompare.general(a, b, modifier);
        }
    },

    /**
     * Compare two strings, sorting empty values to the end by default
     *
     * @param {*} a                 The first string to compare
     * @param {*} b                 The second string to compare
     * @param {Number} modifier     -1 to flip direction, or 1
     * @return {Number}             Either -1, 0, or 1
     */
    string: function(a, b, modifier=1) {
        if (a.length == 0 || b.length == 0) {
            // sort empty values to end (so when users first sort by a
            // column, they can see and find the desired values in that
            // column without scrolling past all the empty values).
            return -(a.length - b.length) * modifier;
        }

        let collator = cal.l10n.createLocaleCollator();
        return collator.compareString(0, a, b) * modifier;
    },

    /**
     * Catch-all function to compare two unknown values. Will return 0.
     *
     * @param {*} a                 The first thing to compare
     * @param {*} b                 The second thing to compare
     * @param {Number} modifier     Provided for consistency, but unused
     * @return {Number}             Will always return 0
     */
    unknown: function(a, b, modifier=1) {
        return 0;
    }
};
