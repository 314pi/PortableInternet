/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

ChromeUtils.import("resource:///modules/mailServices.js");
ChromeUtils.import("resource://calendar/modules/calUtils.jsm");
ChromeUtils.import("resource://gre/modules/Services.jsm");
ChromeUtils.import("resource://gre/modules/XPCOMUtils.jsm");
ChromeUtils.import("resource://gre/modules/Preferences.jsm");
ChromeUtils.import("resource://calendar/modules/ltnInvitationUtils.jsm");

/**
 * Constructor of calItipEmailTransport object
 */
function calItipEmailTransport() {
    this.wrappedJSObject = this;
    this._initEmailTransport();
}
var calItipEmailTransportClassID = Components.ID("{d4d7b59e-c9e0-4a7a-b5e8-5958f85515f0}");
var calItipEmailTransportInterfaces = [Ci.calIItipTransport];
calItipEmailTransport.prototype = {
    classID: calItipEmailTransportClassID,
    QueryInterface: XPCOMUtils.generateQI(calItipEmailTransportInterfaces),
    classInfo: XPCOMUtils.generateCI({
        classID: calItipEmailTransportClassID,
        contractID: "@mozilla.org/calendar/itip-transport;1?type=email",
        classDescription: "Calendar iTIP Email Transport",
        interfaces: calItipEmailTransportInterfaces,
    }),

    mHasXpcomMail: false,
    mDefaultAccount: null,
    mDefaultIdentity: null,
    mDefaultSmtpServer: null,

    get scheme() { return "mailto"; },
    get type() { return "email"; },

    mSenderAddress: null,
    get senderAddress() {
        return this.mSenderAddress;
    },
    set senderAddress(aValue) {
        return (this.mSenderAddress = aValue);
    },

    sendItems: function(aCount, aRecipients, aItipItem) {
        if (this.mHasXpcomMail) {
            cal.LOG("sendItems: Preparing to send an invitation email...");
            let items = this._prepareItems(aItipItem);
            if (items === false) {
                return false;
            }

            return this._sendXpcomMail(aRecipients, items.subject, items.body, aItipItem);
        } else {
            // sending xpcom mail is not available if no identity has been set
            throw Cr.NS_ERROR_NOT_AVAILABLE;
        }
    },

    _prepareItems: function(aItipItem) {
        let item = aItipItem.getItemList({})[0];

        // Get ourselves some default text - when we handle organizer properly
        // We'll need a way to configure the Common Name attribute and we should
        // use it here rather than the email address

        let summary = item.getProperty("SUMMARY") || "";
        let subject = "";
        let body = "";
        switch (aItipItem.responseMethod) {
            case "REQUEST": {
                let usePrefixes = Preferences.get(
                    "calendar.itip.useInvitationSubjectPrefixes",
                    true
                );
                if (usePrefixes) {
                    let seq = item.getProperty("SEQUENCE");
                    let subjectKey = seq && seq > 0
                        ? "itipRequestUpdatedSubject"
                        : "itipRequestSubject";
                    subject = cal.l10n.getLtnString(subjectKey, [summary]);
                } else {
                    subject = summary;
                }
                body = cal.l10n.getLtnString(
                    "itipRequestBody",
                    [item.organizer ? item.organizer.toString() : "", summary]
                );
                break;
            }
            case "CANCEL": {
                subject = cal.l10n.getLtnString("itipCancelSubject", [summary]);
                body = cal.l10n.getLtnString(
                    "itipCancelBody",
                    [item.organizer ? item.organizer.toString() : "", summary]
                );
                break;
            }
            case "DECLINECOUNTER": {
                subject = cal.l10n.getLtnString("itipDeclineCounterSubject", [summary]);
                body = cal.l10n.getLtnString(
                    "itipDeclineCounterBody",
                    [item.organizer ? item.organizer.toString() : "", summary]
                );
                break;
            }
            case "REPLY": {
                // Get my participation status
                let att = cal.itip.getInvitedAttendee(item, aItipItem.targetCalendar);
                if (!att && aItipItem.identity) {
                    att = item.getAttendeeById(cal.email.prependMailTo(aItipItem.identity));
                }
                if (!att) { // should not happen anymore
                    return false;
                }

                // work around BUG 351589, the below just removes RSVP:
                aItipItem.setAttendeeStatus(att.id, att.participationStatus);
                let myPartStat = att.participationStatus;
                let name = att.toString();

                // Generate proper body from my participation status
                let subjectKey, bodyKey;
                switch (myPartStat) {
                    case "ACCEPTED":
                        subjectKey = "itipReplySubjectAccept";
                        bodyKey = "itipReplyBodyAccept";
                        break;
                    case "TENTATIVE":
                        subjectKey = "itipReplySubjectTentative";
                        bodyKey = "itipReplyBodyAccept";
                        break;
                    case "DECLINED":
                        subjectKey = "itipReplySubjectDecline";
                        bodyKey = "itipReplyBodyDecline";
                        break;
                    default:
                        subjectKey = "itipReplySubject";
                        bodyKey = "itipReplyBodyAccept";
                        break;
                }
                subject = cal.l10n.getLtnString(subjectKey, [summary]);
                body = cal.l10n.getLtnString(bodyKey, [name]);
                break;
            }
        }

        return {
            subject: subject,
            body: body
        };
    },

    _initEmailTransport: function() {
        this.mHasXpcomMail = true;

        try {
            this.mDefaultSmtpServer = MailServices.smtp.defaultServer;
            this.mDefaultAccount = MailServices.accounts.defaultAccount;
            this.mDefaultIdentity = this.mDefaultAccount.defaultIdentity;

            if (!this.mDefaultIdentity) {
                // If there isn't a default identity (i.e Local Folders is your
                // default identity, then go ahead and use the first available
                // identity.
                let allIdentities = MailServices.accounts.allIdentities;
                if (allIdentities.length > 0) {
                    this.mDefaultIdentity = allIdentities.queryElementAt(0, Ci.nsIMsgIdentity);
                } else {
                    // If there are no identities, then we are in the same
                    // situation as if we didn't have Xpcom Mail.
                    this.mHasXpcomMail = false;
                    cal.LOG("initEmailService: No XPCOM Mail available: " + e);
                }
            }
        } catch (ex) {
            // Then we must resort to operating system specific means
            this.mHasXpcomMail = false;
        }
    },

    _sendXpcomMail: function(aToList, aSubject, aBody, aItipItem) {
        let identity = null;
        let account;
        if (aItipItem.targetCalendar) {
            identity = aItipItem.targetCalendar.getProperty("imip.identity");
            if (identity) {
                identity = identity.QueryInterface(Ci.nsIMsgIdentity);
                account = aItipItem.targetCalendar
                                   .getProperty("imip.account")
                                   .QueryInterface(Ci.nsIMsgAccount);
            } else {
                cal.WARN("No email identity configured for calendar " +
                         aItipItem.targetCalendar.name);
            }
        }
        if (!identity) { // use some default identity/account:
            identity = this.mDefaultIdentity;
            account = this.mDefaultAccount;
        }

        switch (aItipItem.autoResponse) {
            case Ci.calIItipItem.USER: {
                cal.LOG("sendXpcomMail: Found USER autoResponse type.");
                // We still need this as a last resort if a user just deletes or
                //  drags an invitation related event
                let parent = Services.wm.getMostRecentWindow(null);
                if (parent.closed) {
                    parent = cal.window.getCalendarWindow();
                }
                let cancelled = Services.prompt.confirmEx(
                    parent,
                    cal.l10n.getLtnString("imipSendMail.title"),
                    cal.l10n.getLtnString("imipSendMail.text"),
                    Services.prompt.STD_YES_NO_BUTTONS,
                    null,
                    null,
                    null,
                    null,
                    {}
                );
                if (cancelled) {
                    cal.LOG("sendXpcomMail: Sending of invitation email aborted by user!");
                    break;
                } // else go on with auto sending for now
            }
            // falls through intended
            case Ci.calIItipItem.AUTO: {
                // don't show log message in case of falling through
                if (aItipItem.autoResponse == Ci.calIItipItem.AUTO) {
                    cal.LOG("sendXpcomMail: Found AUTO autoResponse type.");
                }
                let cbEmail = function(aVal, aInd, aArr) {
                    let email = cal.email.getAttendeeEmail(aVal, true);
                    if (!email.length) {
                        cal.LOG("sendXpcomMail: Invalid recipient for email transport: " + aVal.toString());
                    }
                    return email;
                };
                let toMap = aToList.map(cbEmail).filter(value => value.length);
                if (toMap.length < aToList.length) {
                    // at least one invalid recipient, so we skip sending for this message
                    return false;
                }
                let toList = toMap.join(", ");
                let composeUtils = Cc["@mozilla.org/messengercompose/computils;1"]
                                   .createInstance(Ci.nsIMsgCompUtils);
                let messageId = composeUtils.msgGenerateMessageId(identity);
                let mailFile = this._createTempImipFile(toList, aSubject, aBody, aItipItem, identity, messageId);
                if (mailFile) {
                    // compose fields for message: from/to etc need to be specified both here and in the file
                    let composeFields = Cc["@mozilla.org/messengercompose/composefields;1"]
                                        .createInstance(Ci.nsIMsgCompFields);
                    composeFields.characterSet = "UTF-8";
                    composeFields.to = toList;
                    let mailfrom = (identity.fullName.length ? identity.fullName + " <" + identity.email + ">" : identity.email);
                    composeFields.from = (cal.email.validateRecipientList(mailfrom) == mailfrom ? mailfrom : identity.email);
                    composeFields.replyTo = identity.replyTo;
                    composeFields.organization = identity.organization;
                    composeFields.messageId = messageId;
                    let validRecipients;
                    if (identity.doCc) {
                        validRecipients = cal.email.validateRecipientList(identity.doCcList);
                        if (validRecipients != "") {
                            // eslint-disable-next-line id-length
                            composeFields.cc = validRecipients;
                        }
                    }
                    if (identity.doBcc) {
                        validRecipients = cal.email.validateRecipientList(identity.doBccList);
                        if (validRecipients != "") {
                            composeFields.bcc = validRecipients;
                        }
                    }

                    // xxx todo: add send/progress UI, maybe recycle
                    //           "@mozilla.org/messengercompose/composesendlistener;1"
                    //           and/or "chrome://messenger/content/messengercompose/sendProgress.xul"
                    // i.e. bug 432662
                    let msgSend = Cc["@mozilla.org/messengercompose/send;1"]
                                  .createInstance(Ci.nsIMsgSend);
                    msgSend.sendMessageFile(identity,
                                            account.key,
                                            composeFields,
                                            mailFile,
                                            true,  // deleteSendFileOnCompletion
                                            false, // digest_p
                                            (Services.io.offline ? Ci.nsIMsgSend.nsMsgQueueForLater
                                                    : Ci.nsIMsgSend.nsMsgDeliverNow),
                                            null,  // nsIMsgDBHdr msgToReplace
                                            null,  // nsIMsgSendListener aListener
                                            null,  // nsIMsgStatusFeedback aStatusFeedback
                                            "");   // password
                    return true;
                }
                break;
            }
            case Ci.calIItipItem.NONE: {
                // we shouldn't get here, as we stoppped processing in this case
                // earlier in checkAndSend in calItipUtils.jsm
                cal.LOG("sendXpcomMail: Found NONE autoResponse type.");
                break;
            }
            default: {
                // Also of this case should have been taken care at the same place
                throw new Error("sendXpcomMail: " +
                                "Unknown autoResponse type: " +
                                aItipItem.autoResponse);
            }
        }
        return false;
    },

    _createTempImipFile: function(aToList, aSubject, aBody, aItipItem, aIdentity, aMessageId) {
        try {
            let itemList = aItipItem.getItemList({});
            let serializer = Cc["@mozilla.org/calendar/ics-serializer;1"]
                             .createInstance(Ci.calIIcsSerializer);
            serializer.addItems(itemList, itemList.length);
            let methodProp = cal.getIcsService().createIcalProperty("METHOD");
            methodProp.value = aItipItem.responseMethod;
            serializer.addProperty(methodProp);
            let calText = serializer.serializeToString();
            let utf8CalText = ltn.invitation.encodeUTF8(calText);

            // Home-grown mail composition; I'd love to use nsIMimeEmitter, but it's not clear to me whether
            // it can cope with nested attachments,
            // like multipart/alternative with enclosed text/calendar and text/plain.
            let mailText = ltn.invitation.getHeaderSection(aMessageId, aIdentity, aToList, aSubject);
            mailText += "Content-type: multipart/mixed; boundary=\"Boundary_(ID_qyG4ZdjoAsiZ+Jo19dCbWQ)\"\r\n" +
                        "\r\n\r\n" +
                        "--Boundary_(ID_qyG4ZdjoAsiZ+Jo19dCbWQ)\r\n" +
                        "Content-type: multipart/alternative;\r\n" +
                        " boundary=\"Boundary_(ID_ryU4ZdJoASiZ+Jo21dCbwA)\"\r\n" +
                        "\r\n\r\n" +
                        "--Boundary_(ID_ryU4ZdJoASiZ+Jo21dCbwA)\r\n" +
                        "Content-type: text/plain; charset=UTF-8\r\n" +
                        "Content-transfer-encoding: 8BIT\r\n" +
                        "\r\n" +
                        ltn.invitation.encodeUTF8(aBody) +
                        "\r\n\r\n\r\n" +
                        "--Boundary_(ID_ryU4ZdJoASiZ+Jo21dCbwA)\r\n" +
                        "Content-type: text/calendar; method=" + aItipItem.responseMethod + "; charset=UTF-8\r\n" +
                        "Content-transfer-encoding: 8BIT\r\n" +
                        "\r\n" +
                        utf8CalText +
                        "\r\n\r\n" +
                        "--Boundary_(ID_ryU4ZdJoASiZ+Jo21dCbwA)--\r\n" +
                        "\r\n" +
                        "--Boundary_(ID_qyG4ZdjoAsiZ+Jo19dCbWQ)\r\n" +
                        "Content-type: application/ics; name=invite.ics\r\n" +
                        "Content-transfer-encoding: 8BIT\r\n" +
                        "Content-disposition: attachment; filename=invite.ics\r\n" +
                        "\r\n" +
                        utf8CalText +
                        "\r\n\r\n" +
                        "--Boundary_(ID_qyG4ZdjoAsiZ+Jo19dCbWQ)--\r\n";
            cal.LOG("mail text:\n" + mailText);

            let tempFile = Services.dirsvc.get("TmpD", Ci.nsIFile);
            tempFile.append("itipTemp");
            tempFile.createUnique(Ci.nsIFile.NORMAL_FILE_TYPE,
                                  parseInt("0600", 8));

            let outputStream = Cc["@mozilla.org/network/file-output-stream;1"]
                               .createInstance(Ci.nsIFileOutputStream);
            // Let's write the file - constants from file-utils.js
            const MODE_WRONLY = 0x02;
            const MODE_CREATE = 0x08;
            const MODE_TRUNCATE = 0x20;
            outputStream.init(tempFile,
                              MODE_WRONLY | MODE_CREATE | MODE_TRUNCATE,
                              parseInt("0600", 8),
                              0);
            outputStream.write(mailText, mailText.length);
            outputStream.close();

            cal.LOG("_createTempImipFile path: " + tempFile.path);
            return tempFile;
        } catch (exc) {
            cal.ASSERT(false, exc);
            return null;
        }
    }
};

this.NSGetFactory = XPCOMUtils.generateNSGetFactory([calItipEmailTransport]);
