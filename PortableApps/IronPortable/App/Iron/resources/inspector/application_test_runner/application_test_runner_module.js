ApplicationTestRunner.createAndNavigateIFrame=function(url,callback){TestRunner.addSniffer(SDK.ResourceTreeModel.prototype,'_frameNavigated',frameNavigated);TestRunner.evaluateInPageAnonymously('createAndNavigateIFrame(unescape(\''+escape(url)+'\'))');function frameNavigated(frame){callback(frame.id);}};ApplicationTestRunner.navigateIFrame=function(frameId,url,callback){var frame=TestRunner.resourceTreeModel.frameForId(frameId);TestRunner.evaluateInPageAnonymously('navigateIFrame(unescape(\''+escape(frame.name)+'\'), unescape(\''+escape(url)+'\'))');TestRunner.addSniffer(SDK.ResourceTreeModel.prototype,'_frameNavigated',frameNavigated);function frameNavigated(frame){callback(frame.id);}};ApplicationTestRunner.removeIFrame=function(frameId,callback){var frame=TestRunner.resourceTreeModel.frameForId(frameId);TestRunner.evaluateInPageAnonymously('removeIFrame(unescape(\''+escape(frame.name)+'\'))');TestRunner.addSniffer(SDK.ResourceTreeModel.prototype,'_frameDetached',frameDetached);function frameDetached(frame){callback(frame.id);}};ApplicationTestRunner.swapFrameCache=function(frameId){var frame=TestRunner.resourceTreeModel.frameForId(frameId);TestRunner.evaluateInPageAnonymously('swapFrameCache(unescape(\''+escape(frame.name)+'\'))');};ApplicationTestRunner.dumpApplicationCache=function(){ApplicationTestRunner.dumpApplicationCacheTree();ApplicationTestRunner.dumpApplicationCacheModel();TestRunner.addResult('');};ApplicationTestRunner.dumpApplicationCacheTree=function(){TestRunner.addResult('Dumping application cache tree:');var applicationCacheTreeElement=UI.panels.resources._sidebar.applicationCacheListTreeElement;if(!applicationCacheTreeElement.childCount()){TestRunner.addResult('    (empty)');return;}
for(var i=0;i<applicationCacheTreeElement.childCount();++i){var manifestTreeElement=applicationCacheTreeElement.childAt(i);TestRunner.addResult('    Manifest URL: '+manifestTreeElement.manifestURL);if(!manifestTreeElement.childCount()){TestRunner.addResult('    (no frames)');continue;}
for(var j=0;j<manifestTreeElement.childCount();++j){var frameTreeElement=manifestTreeElement.childAt(j);TestRunner.addResult('        Frame: '+frameTreeElement.title);}}};ApplicationTestRunner.frameIdToString=function(frameId){if(!ApplicationTestRunner.framesByFrameId)
ApplicationTestRunner.framesByFrameId={};var frame=TestRunner.resourceTreeModel.frameForId(frameId);if(!frame)
frame=ApplicationTestRunner.framesByFrameId[frameId];ApplicationTestRunner.framesByFrameId[frameId]=frame;return frame.name;};ApplicationTestRunner.applicationCacheStatusToString=function(status){var statusInformation={};statusInformation[applicationCache.UNCACHED]='UNCACHED';statusInformation[applicationCache.IDLE]='IDLE';statusInformation[applicationCache.CHECKING]='CHECKING';statusInformation[applicationCache.DOWNLOADING]='DOWNLOADING';statusInformation[applicationCache.UPDATEREADY]='UPDATEREADY';statusInformation[applicationCache.OBSOLETE]='OBSOLETE';return statusInformation[status]||statusInformation[applicationCache.UNCACHED];};ApplicationTestRunner.dumpApplicationCacheModel=function(){TestRunner.addResult('Dumping application cache model:');var model=UI.panels.resources._sidebar._applicationCacheModel;var frameIds=[];for(var frameId in model._manifestURLsByFrame)
frameIds.push(frameId);function compareFunc(a,b){return ApplicationTestRunner.frameIdToString(a).localeCompare(ApplicationTestRunner.frameIdToString(b));}
frameIds.sort(compareFunc);if(!frameIds.length){TestRunner.addResult('    (empty)');return;}
for(var i=0;i<frameIds.length;++i){var frameId=frameIds[i];var manifestURL=model.frameManifestURL(frameId);var status=model.frameManifestStatus(frameId);TestRunner.addResult('    Frame: '+ApplicationTestRunner.frameIdToString(frameId));TestRunner.addResult('        manifest url: '+manifestURL);TestRunner.addResult('        status:       '+ApplicationTestRunner.applicationCacheStatusToString(status));}};ApplicationTestRunner.waitForFrameManifestURLAndStatus=function(frameId,manifestURL,status,callback){var frameManifestStatus=UI.panels.resources._sidebar._applicationCacheModel.frameManifestStatus(frameId);var frameManifestURL=UI.panels.resources._sidebar._applicationCacheModel.frameManifestURL(frameId);if(frameManifestStatus===status&&frameManifestURL.indexOf(manifestURL)!==-1){callback();return;}
var handler=ApplicationTestRunner.waitForFrameManifestURLAndStatus.bind(this,frameId,manifestURL,status,callback);TestRunner.addSniffer(Resources.ApplicationCacheModel.prototype,'_frameManifestUpdated',handler);};ApplicationTestRunner.startApplicationCacheStatusesRecording=function(){if(ApplicationTestRunner.applicationCacheStatusesRecords){ApplicationTestRunner.applicationCacheStatusesRecords={};return;}
ApplicationTestRunner.applicationCacheStatusesRecords={};function addRecord(frameId,manifestURL,status){var record={};record.manifestURL=manifestURL;record.status=status;if(!ApplicationTestRunner.applicationCacheStatusesRecords[frameId])
ApplicationTestRunner.applicationCacheStatusesRecords[frameId]=[];ApplicationTestRunner.applicationCacheStatusesRecords[frameId].push(record);if(ApplicationTestRunner.awaitedFrameStatusEventsCount&&ApplicationTestRunner.awaitedFrameStatusEventsCount[frameId]){ApplicationTestRunner.awaitedFrameStatusEventsCount[frameId].count--;if(!ApplicationTestRunner.awaitedFrameStatusEventsCount[frameId].count)
ApplicationTestRunner.awaitedFrameStatusEventsCount[frameId].callback();}}
TestRunner.addSniffer(Resources.ApplicationCacheModel.prototype,'_frameManifestUpdated',addRecord,true);};ApplicationTestRunner.ensureFrameStatusEventsReceived=function(frameId,count,callback){var records=ApplicationTestRunner.applicationCacheStatusesRecords[frameId]||[];var eventsLeft=count-records.length;if(!eventsLeft){callback();return;}
if(!ApplicationTestRunner.awaitedFrameStatusEventsCount)
ApplicationTestRunner.awaitedFrameStatusEventsCount={};ApplicationTestRunner.awaitedFrameStatusEventsCount[frameId]={count:eventsLeft,callback:callback};};TestRunner.deprecatedInitAsync(`
  var framesCount = 0;

  function createAndNavigateIFrame(url) {
    var iframe = document.createElement('iframe');
    iframe.src = url;
    iframe.name = 'frame' + ++framesCount;
    iframe.id = iframe.name;
    document.body.appendChild(iframe);
  }

  function removeIFrame(name) {
    var iframe = document.querySelector('#' + name);
    iframe.parentElement.removeChild(iframe);
  }

  function navigateIFrame(name, url) {
    var iframe = document.querySelector('#' + name);
    iframe.src = url;
  }

  function swapFrameCache(name) {
    var iframe = document.querySelector('#' + name);
    iframe.contentWindow.applicationCache.swapCache();
  }
`);;ApplicationTestRunner.dumpCacheTree=async function(){UI.panels.resources._sidebar.cacheStorageListTreeElement.expand();var promise=TestRunner.addSnifferPromise(SDK.ServiceWorkerCacheModel.prototype,'_updateCacheNames');UI.panels.resources._sidebar.cacheStorageListTreeElement._refreshCaches();await promise;await ApplicationTestRunner.dumpCacheTreeNoRefresh();};ApplicationTestRunner.dumpCacheTreeNoRefresh=async function(){UI.panels.resources._sidebar.cacheStorageListTreeElement.expand();TestRunner.addResult('Dumping CacheStorage tree:');var cachesTreeElement=UI.panels.resources._sidebar.cacheStorageListTreeElement;if(!cachesTreeElement.childCount()){TestRunner.addResult('    (empty)');return;}
for(var i=0;i<cachesTreeElement.childCount();++i){var cacheTreeElement=cachesTreeElement.childAt(i);TestRunner.addResult('    cache: '+cacheTreeElement.title);var view=cacheTreeElement._view;promise=TestRunner.addSnifferPromise(Resources.ServiceWorkerCacheView.prototype,'_updateDataCallback');if(!view)
cacheTreeElement.onselect(false);else
view._updateData(true);view=cacheTreeElement._view;await promise;if(view._entriesForTest.length===0){TestRunner.addResult('        (cache empty)');continue;}
var dataGrid=view._dataGrid;for(var node of dataGrid.rootNode().children){var children=Array.from(node.element().children).filter(function(element){return!element.classList.contains('responseTime-column');});var entries=Array.from(children,td=>td.textContent).filter(text=>text);TestRunner.addResult('        '+entries.join(', '));}}};ApplicationTestRunner.deleteCacheFromInspector=async function(cacheName,optionalEntry){UI.panels.resources._sidebar.cacheStorageListTreeElement.expand();if(optionalEntry)
TestRunner.addResult('Deleting CacheStorage entry '+optionalEntry+' in cache '+cacheName);else
TestRunner.addResult('Deleting CacheStorage cache '+cacheName);var cachesTreeElement=UI.panels.resources._sidebar.cacheStorageListTreeElement;var promise=TestRunner.addSnifferPromise(SDK.ServiceWorkerCacheModel.prototype,'_updateCacheNames');UI.panels.resources._sidebar.cacheStorageListTreeElement._refreshCaches();await promise;if(!cachesTreeElement.childCount())
throw'Error: Could not find CacheStorage cache '+cacheName;for(var i=0;i<cachesTreeElement.childCount();i++){var cacheTreeElement=cachesTreeElement.childAt(i);var title=cacheTreeElement.title;var elementCacheName=title.substring(0,title.lastIndexOf(' - '));if(elementCacheName!==cacheName)
continue;if(!optionalEntry){promise=TestRunner.addSnifferPromise(SDK.ServiceWorkerCacheModel.prototype,'_cacheRemoved');cacheTreeElement._clearCache();await promise;return;}
promise=TestRunner.addSnifferPromise(Resources.ServiceWorkerCacheView.prototype,'_updateDataCallback');var view=cacheTreeElement._view;if(!view)
cacheTreeElement.onselect(false);else
view._updateData(true);view=cacheTreeElement._view;await promise;var entry=view._entriesForTest.find(entry=>entry.requestURL===optionalEntry);if(!entry)
throw'Error: Could not find cache entry to delete: '+optionalEntry;await view._model.deleteCacheEntry(view._cache,entry.requestURL);return;}
throw'Error: Could not find CacheStorage cache '+cacheName;};ApplicationTestRunner.waitForCacheRefresh=function(callback){TestRunner.addSniffer(SDK.ServiceWorkerCacheModel.prototype,'_updateCacheNames',callback,false);};ApplicationTestRunner.createCache=function(cacheName){return TestRunner.callFunctionInPageAsync('createCache',[cacheName]);};ApplicationTestRunner.addCacheEntry=function(cacheName,requestUrl,responseText){return TestRunner.callFunctionInPageAsync('addCacheEntry',[cacheName,requestUrl,responseText]);};ApplicationTestRunner.deleteCache=function(cacheName){return TestRunner.callFunctionInPageAsync('deleteCache',[cacheName]);};ApplicationTestRunner.deleteCacheEntry=function(cacheName,requestUrl){return TestRunner.callFunctionInPageAsync('deleteCacheEntry',[cacheName,requestUrl]);};ApplicationTestRunner.clearAllCaches=function(){return TestRunner.callFunctionInPageAsync('clearAllCaches');};TestRunner.deprecatedInitAsync(`
  function onCacheStorageError(e) {
    console.error('CacheStorage error: ' + e);
  }

  function createCache(cacheName) {
    return caches.open(cacheName).catch(onCacheStorageError);
  }

  function addCacheEntry(cacheName, requestUrl, responseText) {
    return caches.open(cacheName).then(function(cache) {
      var request = new Request(requestUrl);
      var myBlob = new Blob();

      var init = {
        'status': 200,
        'statusText': responseText
      };

      var response = new Response(myBlob, init);
      return cache.put(request, response);
    }).catch(onCacheStorageError);
  }

  function deleteCache(cacheName) {
    return caches.delete(cacheName).then(function(success) {
      if (!success)
        onCacheStorageError('Could not find cache ' + cacheName);
    }).catch(onCacheStorageError);
  }

  function deleteCacheEntry(cacheName, requestUrl) {
    return caches.open(cacheName).then(cache => cache.delete(new Request(requestUrl))).catch(onCacheStorageError);
  }

  function clearAllCaches() {
    return caches.keys().then(keys => Promise.all(keys.map(key => caches.delete(key)))).catch(onCacheStorageError.bind(this, undefined));
  }
`);;ApplicationTestRunner.dumpIndexedDBTree=function(){TestRunner.addResult('Dumping IndexedDB tree:');var indexedDBTreeElement=UI.panels.resources._sidebar.indexedDBListTreeElement;if(!indexedDBTreeElement.childCount()){TestRunner.addResult('    (empty)');return;}
for(var i=0;i<indexedDBTreeElement.childCount();++i){var databaseTreeElement=indexedDBTreeElement.childAt(i);TestRunner.addResult('    database: '+databaseTreeElement.title);if(!databaseTreeElement.childCount()){TestRunner.addResult('        (no object stores)');continue;}
for(var j=0;j<databaseTreeElement.childCount();++j){var objectStoreTreeElement=databaseTreeElement.childAt(j);TestRunner.addResult('        Object store: '+objectStoreTreeElement.title);if(!objectStoreTreeElement.childCount()){TestRunner.addResult('            (no indexes)');continue;}
for(var k=0;k<objectStoreTreeElement.childCount();++k){var indexTreeElement=objectStoreTreeElement.childAt(k);TestRunner.addResult('            Index: '+indexTreeElement.title);}}}};ApplicationTestRunner.dumpObjectStores=function(){TestRunner.addResult('Dumping ObjectStore data:');let idbDatabaseTreeElement=UI.panels.resources._sidebar.indexedDBListTreeElement._idbDatabaseTreeElements[0];for(let i=0;i<idbDatabaseTreeElement.childCount();++i){let objectStoreTreeElement=idbDatabaseTreeElement.childAt(i);objectStoreTreeElement.onselect(false);TestRunner.addResult('    Object store: '+objectStoreTreeElement.title);let entries=objectStoreTreeElement._view._entries;TestRunner.addResult('            Number of entries: '+entries.length);for(let j=0;j<entries.length;++j)
TestRunner.addResult('            Key = '+entries[j].key._value+', value = '+entries[j].value);for(let k=0;k<objectStoreTreeElement.childCount();++k){let indexTreeElement=objectStoreTreeElement.childAt(k);TestRunner.addResult('            Index: '+indexTreeElement.title);indexTreeElement.onselect(false);let entries=indexTreeElement._view._entries;TestRunner.addResult('                Number of entries: '+entries.length);for(let j=0;j<entries.length;++j)
TestRunner.addResult('                Key = '+entries[j].primaryKey._value+', value = '+entries[j].value);}}};var lastCallbackId=0;var callbacks={};var callbackIdPrefix='InspectorTest.IndexedDB_callback';ApplicationTestRunner.evaluateWithCallback=function(frameId,methodName,parameters,callback){ApplicationTestRunner._installIndexedDBSniffer();var callbackId=++lastCallbackId;callbacks[callbackId]=callback;var parametersString='dispatchCallback.bind(this, "'+callbackIdPrefix+callbackId+'")';for(var i=0;i<parameters.length;++i)
parametersString+=', '+JSON.stringify(parameters[i]);var requestString=methodName+'('+parametersString+')';TestRunner.evaluateInPageAnonymously(requestString);};ApplicationTestRunner._installIndexedDBSniffer=function(){ConsoleTestRunner.addConsoleSniffer(consoleMessageOverride,false);function consoleMessageOverride(msg){var text=msg.messageText;if(!text.startsWith(callbackIdPrefix)){ConsoleTestRunner.addConsoleSniffer(consoleMessageOverride,false);return;}
var callbackId=text.substring(callbackIdPrefix.length);callbacks[callbackId].call();delete callbacks[callbackId];}};ApplicationTestRunner.createDatabase=function(frameId,databaseName,callback){ApplicationTestRunner.evaluateWithCallback(frameId,'createDatabase',[databaseName],callback);};ApplicationTestRunner.deleteDatabase=function(frameId,databaseName,callback){ApplicationTestRunner.evaluateWithCallback(frameId,'deleteDatabase',[databaseName],callback);};ApplicationTestRunner.createObjectStore=function(frameId,databaseName,objectStoreName,keyPath,autoIncrement,callback){ApplicationTestRunner.evaluateWithCallback(frameId,'createObjectStore',[databaseName,objectStoreName,keyPath,autoIncrement],callback);};ApplicationTestRunner.deleteObjectStore=function(frameId,databaseName,objectStoreName,callback){ApplicationTestRunner.evaluateWithCallback(frameId,'deleteObjectStore',[databaseName,objectStoreName],callback);};ApplicationTestRunner.createObjectStoreIndex=function(frameId,databaseName,objectStoreName,objectStoreIndexName,keyPath,unique,multiEntry,callback){ApplicationTestRunner.evaluateWithCallback(frameId,'createObjectStoreIndex',[databaseName,objectStoreName,objectStoreIndexName,keyPath,unique,multiEntry],callback);};ApplicationTestRunner.deleteObjectStoreIndex=function(frameId,databaseName,objectStoreName,objectStoreIndexName,callback){ApplicationTestRunner.evaluateWithCallback(frameId,'deleteObjectStoreIndex',[databaseName,objectStoreName,objectStoreIndexName],callback);};ApplicationTestRunner.addIDBValue=function(frameId,databaseName,objectStoreName,value,key,callback){ApplicationTestRunner.evaluateWithCallback(frameId,'addIDBValue',[databaseName,objectStoreName,value,key],callback);};ApplicationTestRunner.createIndexedDBModel=function(){var indexedDBModel=new Resources.IndexedDBModel(SDK.targetManager.mainTarget(),TestRunner.securityOriginManager);indexedDBModel.enable();return indexedDBModel;};ApplicationTestRunner.createDatabaseAsync=function(databaseName){return TestRunner.evaluateInPageAsync('createDatabaseAsync(\''+databaseName+'\')');};ApplicationTestRunner.deleteDatabaseAsync=function(databaseName){return TestRunner.evaluateInPageAsync('deleteDatabaseAsync(\''+databaseName+'\')');};ApplicationTestRunner.createObjectStoreAsync=function(databaseName,objectStoreName,indexName){return TestRunner.evaluateInPageAsync('createObjectStoreAsync(\''+databaseName+'\', \''+objectStoreName+'\', \''+indexName+'\')');};ApplicationTestRunner.deleteObjectStoreAsync=function(databaseName,objectStoreName){return TestRunner.evaluateInPageAsync('deleteObjectStoreAsync(\''+databaseName+'\', \''+objectStoreName+'\')');};ApplicationTestRunner.createObjectStoreIndexAsync=function(databaseName,objectStoreName,indexName){return TestRunner.evaluateInPageAsync('createObjectStoreIndexAsync(\''+databaseName+'\', \''+objectStoreName+'\', \''+indexName+'\')');};ApplicationTestRunner.deleteObjectStoreIndexAsync=function(databaseName,objectStoreName,indexName){return TestRunner.evaluateInPageAsync('deleteObjectStoreIndexAsync(\''+databaseName+'\', \''+objectStoreName+'\', \''+indexName+'\')');};ApplicationTestRunner.addIDBValueAsync=function(databaseName,objectStoreName,key,value){return TestRunner.evaluateInPageAsync('addIDBValueAsync(\''+databaseName+'\', \''+objectStoreName+'\', \''+key+'\', \''+value+'\')');};ApplicationTestRunner.deleteIDBValueAsync=function(databaseName,objectStoreName,key){return TestRunner.evaluateInPageAsync('deleteIDBValueAsync(\''+databaseName+'\', \''+objectStoreName+'\', \''+key+'\')');};TestRunner.deprecatedInitAsync(`
  function dispatchCallback(callbackId) {
    console.log(callbackId);
  }

  function onIndexedDBError(e) {
    console.error('IndexedDB error: ' + e);
  }

  function onIndexedDBBlocked(e) {
    console.error('IndexedDB blocked: ' + e);
  }

  function doWithDatabase(databaseName, callback) {
    function innerCallback() {
      var db = request.result;
      callback(db);
    }

    var request = indexedDB.open(databaseName);
    request.onblocked = onIndexedDBBlocked;
    request.onerror = onIndexedDBError;
    request.onsuccess = innerCallback;
  }

  function doWithVersionTransaction(databaseName, callback, commitCallback) {
    doWithDatabase(databaseName, step2);

    function step2(db) {
      var version = db.version;
      db.close();
      request = indexedDB.open(databaseName, version + 1);
      request.onerror = onIndexedDBError;
      request.onupgradeneeded = onUpgradeNeeded;
      request.onsuccess = onOpened;

      function onUpgradeNeeded(e) {
        var db = e.target.result;
        var trans = e.target.transaction;
        callback(db, trans);
      }

      function onOpened(e) {
        var db = e.target.result;
        db.close();
        commitCallback();
      }
    }
  }

  function doWithReadWriteTransaction(databaseName, objectStoreName, callback, commitCallback) {
    doWithDatabase(databaseName, step2);

    function step2(db) {
      var transaction = db.transaction([objectStoreName], 'readwrite');
      var objectStore = transaction.objectStore(objectStoreName);
      callback(objectStore, innerCommitCallback);

      function innerCommitCallback() {
        db.close();
        commitCallback();
      }
    }
  }

  function createDatabase(callback, databaseName) {
    var request = indexedDB.open(databaseName);
    request.onerror = onIndexedDBError;
    request.onsuccess = closeDatabase;

    function closeDatabase() {
      request.result.close();
      callback();
    }
  }

  function deleteDatabase(callback, databaseName) {
    var request = indexedDB.deleteDatabase(databaseName);
    request.onerror = onIndexedDBError;
    request.onsuccess = callback;
  }

  function createObjectStore(callback, databaseName, objectStoreName, keyPath, autoIncrement) {
    doWithVersionTransaction(databaseName, withTransactionCallback, callback);

    function withTransactionCallback(db, transaction) {
      var store = db.createObjectStore(objectStoreName, {
        keyPath: keyPath,
        autoIncrement: autoIncrement
      });
    }
  }

  function deleteObjectStore(callback, databaseName, objectStoreName) {
    doWithVersionTransaction(databaseName, withTransactionCallback, callback);

    function withTransactionCallback(db, transaction) {
      var store = db.deleteObjectStore(objectStoreName);
    }
  }

  function createObjectStoreIndex(callback, databaseName, objectStoreName, objectStoreIndexName, keyPath, unique, multiEntry) {
    doWithVersionTransaction(databaseName, withTransactionCallback, callback);

    function withTransactionCallback(db, transaction) {
      var objectStore = transaction.objectStore(objectStoreName);

      objectStore.createIndex(objectStoreIndexName, keyPath, {
        unique: unique,
        multiEntry: multiEntry
      });
    }
  }

  function deleteObjectStoreIndex(callback, databaseName, objectStoreName, objectStoreIndexName) {
    doWithVersionTransaction(databaseName, withTransactionCallback, callback);

    function withTransactionCallback(db, transaction) {
      var objectStore = transaction.objectStore(objectStoreName);
      objectStore.deleteIndex(objectStoreIndexName);
    }
  }

  function addIDBValue(callback, databaseName, objectStoreName, value, key) {
    doWithReadWriteTransaction(databaseName, objectStoreName, withTransactionCallback, callback);

    function withTransactionCallback(objectStore, commitCallback) {
      var request;

      if (key)
        request = objectStore.add(value, key);
      else
        request = objectStore.add(value);

      request.onerror = onIndexedDBError;
      request.onsuccess = commitCallback;
    }
  }

  function createDatabaseAsync(databaseName) {
    return new Promise((resolve) => {
      createDatabase(resolve, databaseName);
    });
  }

  function upgradeRequestAsync(databaseName, onUpgradeNeeded, callback) {
    var request = indexedDB.open(databaseName);
    request.onerror = onIndexedDBError;
    request.onsuccess = function(event) {
      var db = request.result;
      var version = db.version;
      db.close();

      var upgradeRequest = indexedDB.open(databaseName, version + 1);
      upgradeRequest.onerror = onIndexedDBError;
      upgradeRequest.onupgradeneeded = function(e) {
        onUpgradeNeeded(e.target.result, e.target.transaction, callback);
      }
      upgradeRequest.onsuccess = function(e) {
        var upgradeDb = e.target.result;
        upgradeDb.close();
        callback();
      }
    }
  }

  function deleteDatabaseAsync(databaseName) {
    var callback;
    var promise = new Promise((fulfill) => callback = fulfill);
    var request = indexedDB.deleteDatabase(databaseName);
    request.onerror = onIndexedDBError;
    request.onsuccess = callback;
    return promise;
  }

  function createObjectStoreAsync(databaseName, objectStoreName, indexName) {
    var callback;
    var promise = new Promise((fulfill) => callback = fulfill);
    var onUpgradeNeeded = function(upgradeDb, transaction, callback) {
      var store = upgradeDb.createObjectStore(objectStoreName, { keyPath: "test", autoIncrement: false });
      store.createIndex(indexName, "test", { unique: false, multiEntry: false });
      callback();
    }
    upgradeRequestAsync(databaseName, onUpgradeNeeded, callback)
    return promise;
  }

  function deleteObjectStoreAsync(databaseName, objectStoreName) {
    var callback;
    var promise = new Promise((fulfill) => callback = fulfill);
    var onUpgradeNeeded = function(upgradeDb, transaction, callback) {
      upgradeDb.deleteObjectStore(objectStoreName);
      callback();
    }
    upgradeRequestAsync(databaseName, onUpgradeNeeded, callback)
    return promise;
  }

  function createObjectStoreIndexAsync(databaseName, objectStoreName, indexName) {
    var callback;
    var promise = new Promise((fulfill) => callback = fulfill);
    var onUpgradeNeeded = function(upgradeDb, transaction, callback) {
      var store = transaction.objectStore(objectStoreName);
      store.createIndex(indexName, "test", { unique: false, multiEntry: false });
      callback();
    }
    upgradeRequestAsync(databaseName, onUpgradeNeeded, callback)
    return promise;
  }

  function deleteObjectStoreIndexAsync(databaseName, objectStoreName, indexName) {
    var callback;
    var promise = new Promise((fulfill) => callback = fulfill);
    var onUpgradeNeeded = function(upgradeDb, transaction, callback) {
      var store = transaction.objectStore(objectStoreName);
      store.deleteIndex(indexName);
      callback();
    }
    upgradeRequestAsync(databaseName, onUpgradeNeeded, callback)
    return promise;
  }

  function addIDBValueAsync(databaseName, objectStoreName, key, value) {
    var callback;
    var promise = new Promise(fulfill => callback = fulfill);
    var request = indexedDB.open(databaseName);
    request.onerror = onIndexedDBError;

    request.onsuccess = function(event) {
      var db = request.result;
      var transaction = db.transaction(objectStoreName, 'readwrite');
      var store = transaction.objectStore(objectStoreName);

      store.put({
        test: key,
        testValue: value
      });

      transaction.onerror = onIndexedDBError;

      transaction.oncomplete = function() {
        db.close();
        callback();
      };
    };

    return promise;
  }

  function deleteIDBValueAsync(databaseName, objectStoreName, key) {
    var callback;
    var promise = new Promise((fulfill) => callback = fulfill);
    var request = indexedDB.open(databaseName);
    request.onerror = onIndexedDBError;
    request.onsuccess = function(event) {
      var db = request.result;
      var transaction = db.transaction(objectStoreName, "readwrite");
      var store = transaction.objectStore(objectStoreName);
      store.delete(key);

      transaction.onerror = onIndexedDBError;
      transaction.oncomplete = function() {
        db.close();
        callback();
      };
    }
    return promise;
  }
`);;ApplicationTestRunner.dumpResources=function(formatter){var results=[];function formatterWrapper(resource){if(formatter)
results.push({resource:resource,text:formatter(resource)});else
results.push({resource:resource,text:resource.url});}
TestRunner.resourceTreeModel.forAllResources(formatterWrapper);function comparator(result1,result2){return result1.resource.url.localeCompare(result2.resource.url);}
results.sort(comparator);for(var i=0;i<results.length;++i)
TestRunner.addResult(results[i].text);};ApplicationTestRunner.dumpResourcesURLMap=function(){var results=[];TestRunner.resourceTreeModel.forAllResources(collect);function collect(resource){results.push({url:resource.url,resource:TestRunner.resourceTreeModel.resourceForURL(resource.url)});}
function comparator(result1,result2){if(result1.url>result2.url)
return 1;if(result2.url>result1.url)
return-1;return 0;}
results.sort(comparator);for(var i=0;i<results.length;++i)
TestRunner.addResult(results[i].url+' == '+results[i].resource.url);};ApplicationTestRunner.dumpResourcesTree=function(){function dump(treeItem,prefix){if(typeof treeItem._resetBubble==='function')
treeItem._resetBubble();TestRunner.addResult(prefix+treeItem.listItemElement.textContent);treeItem.expand();var children=treeItem.children();for(var i=0;children&&i<children.length;++i)
dump(children[i],prefix+'    ');}
dump(UI.panels.resources._sidebar._resourcesSection._treeElement,'');if(!ApplicationTestRunner._testSourceNavigator){ApplicationTestRunner._testSourceNavigator=new Sources.SourcesNavigatorView();ApplicationTestRunner._testSourceNavigator.show(UI.inspectorView.element);}
SourcesTestRunner.dumpNavigatorViewInAllModes(ApplicationTestRunner._testSourceNavigator);};ApplicationTestRunner.dumpResourceTreeEverything=function(){function format(resource){return resource.resourceType().name()+' '+resource.url;}
TestRunner.addResult('Resources:');ApplicationTestRunner.dumpResources(format);TestRunner.addResult('');TestRunner.addResult('Resources URL Map:');ApplicationTestRunner.dumpResourcesURLMap();TestRunner.addResult('');TestRunner.addResult('Resources Tree:');ApplicationTestRunner.dumpResourcesTree();};;ApplicationTestRunner.resetState=async function(){var securityOrigin=new Common.ParsedURL(TestRunner.url()).securityOrigin();var storageTypes=['appcache','cache_storage','cookies','indexeddb','local_storage','service_workers','websql'];await TestRunner.mainTarget.storageAgent().clearDataForOrigin(securityOrigin,storageTypes.join(','));};ApplicationTestRunner.createWebSQLDatabase=function(name){return TestRunner.evaluateInPageAsync(`_openWebSQLDatabase("${name}")`);};ApplicationTestRunner.requestURLComparer=function(r1,r2){return r1.request.url.localeCompare(r2.request.url);};ApplicationTestRunner.runAfterCachedResourcesProcessed=function(callback){if(!TestRunner.resourceTreeModel._cachedResourcesProcessed)
TestRunner.resourceTreeModel.addEventListener(SDK.ResourceTreeModel.Events.CachedResourcesLoaded,callback);else
callback();};ApplicationTestRunner.runAfterResourcesAreFinished=function(resourceURLs,callback){var resourceURLsMap=new Set(resourceURLs);function checkResources(){for(var url of resourceURLsMap){var resource=ApplicationTestRunner.resourceMatchingURL(url);if(resource)
resourceURLsMap.delete(url);}
if(!resourceURLsMap.size){TestRunner.resourceTreeModel.removeEventListener(SDK.ResourceTreeModel.Events.ResourceAdded,checkResources);callback();}}
checkResources();if(resourceURLsMap.size)
TestRunner.resourceTreeModel.addEventListener(SDK.ResourceTreeModel.Events.ResourceAdded,checkResources);};ApplicationTestRunner.showResource=function(resourceURL,callback){var reported=false;function callbackWrapper(sourceFrame){if(reported)
return;callback(sourceFrame);reported=true;}
function showResourceCallback(){var resource=ApplicationTestRunner.resourceMatchingURL(resourceURL);if(!resource)
return;UI.panels.resources.showResource(resource,1);var sourceFrame=UI.panels.resources._resourceViewForResource(resource);if(sourceFrame.loaded)
callbackWrapper(sourceFrame);else
TestRunner.addSniffer(sourceFrame,'onTextEditorContentSet',callbackWrapper.bind(null,sourceFrame));}
ApplicationTestRunner.runAfterResourcesAreFinished([resourceURL],showResourceCallback);};ApplicationTestRunner.resourceMatchingURL=function(resourceURL){var result=null;TestRunner.resourceTreeModel.forAllResources(visit);function visit(resource){if(resource.url.indexOf(resourceURL)!==-1){result=resource;return true;}}
return result;};ApplicationTestRunner.databaseModel=function(){return TestRunner.mainTarget.model(Resources.DatabaseModel);};ApplicationTestRunner.domStorageModel=function(){return TestRunner.mainTarget.model(Resources.DOMStorageModel);};ApplicationTestRunner.indexedDBModel=function(){return TestRunner.mainTarget.model(Resources.IndexedDBModel);};TestRunner.deprecatedInitAsync(`
  function _openWebSQLDatabase(name) {
    return new Promise(resolve => openDatabase(name, '1.0', '', 1024 * 1024, resolve));
  }
`);;ApplicationTestRunner.registerServiceWorker=function(script,scope){return TestRunner.callFunctionInPageAsync('registerServiceWorker',[script,scope]);};ApplicationTestRunner.waitForActivated=function(scope){return TestRunner.callFunctionInPageAsync('waitForActivated',[scope]);};ApplicationTestRunner.unregisterServiceWorker=function(scope){return TestRunner.callFunctionInPageAsync('unregisterServiceWorker',[scope]);};ApplicationTestRunner.postToServiceWorker=function(scope,message){return TestRunner.evaluateInPageAnonymously('postToServiceWorker("'+scope+'","'+message+'")');};ApplicationTestRunner.waitForServiceWorker=function(callback){function isRightTarget(target){return TestRunner.isDedicatedWorker(target)&&TestRunner.isServiceWorker(target.parentTarget());}
SDK.targetManager.observeTargets({targetAdded:function(target){if(isRightTarget(target)&&callback){setTimeout(callback.bind(null,target),0);callback=null;}},targetRemoved:function(target){}});};ApplicationTestRunner.dumpServiceWorkersView=function(){var swView=UI.panels.resources.visibleView;return swView._currentWorkersView._sectionList.childTextNodes().concat(swView._otherWorkersView._sectionList.childTextNodes()).map(function(node){return node.textContent.replace(/Received.*/,'Received').replace(/#\d+/,'#N');}).join('\n');};ApplicationTestRunner.deleteServiceWorkerRegistration=function(scope){TestRunner.serviceWorkerManager.registrations().valuesArray().map(function(registration){if(registration.scopeURL===scope)
TestRunner.serviceWorkerManager.deleteRegistration(registration.id);});};ApplicationTestRunner.makeFetchInServiceWorker=function(scope,url,requestInitializer,callback){TestRunner.callFunctionInPageAsync('makeFetchInServiceWorker',[scope,url,requestInitializer]).then(callback);};TestRunner.deprecatedInitAsync(`
  var registrations = {};

  function registerServiceWorker(script, scope) {
    return navigator.serviceWorker.register(script, {
      scope: scope
    })
    .then(reg => registrations[scope] = reg)
    .catch(err => {
      return Promise.reject(new Error('Service Worker registration error: ' +
                                      err.toString()));
    });
  }

  function waitForActivated(scope) {
    let reg = registrations[scope];
    if (!reg)
      return Promise.reject(new Error('The registration'));
    let worker = reg.installing || reg.waiting || reg.active;
    if (worker.state === 'activated')
      return Promise.resolve();
    if (worker.state === 'redundant')
      return Promise.reject(new Error('The worker is redundant'));
    return new Promise(resolve => {
        worker.addEventListener('statechange', () => {
            if (worker.state === 'activated')
              resolve();
          });
      });
  }

  function postToServiceWorker(scope, message) {
    registrations[scope].active.postMessage(message);
  }

  function unregisterServiceWorker(scope) {
    var registration = registrations[scope];

    if (!registration)
      return Promise.reject('ServiceWorker for ' + scope + ' is not registered');

    return registration.unregister().then(() => delete registrations[scope]);
  }

  function makeFetchInServiceWorker(scope, url, requestInitializer) {
    let script = 'resources/network-fetch-worker.js';

    return navigator.serviceWorker.register(script, {
      scope: scope
    }).then(registration => {
      let worker = registration.installing;

      return new Promise(resolve => {
        navigator.serviceWorker.onmessage = e => {
          resolve(e.data);
        };

        worker.postMessage({
          url: url,
          init: requestInitializer
        });
      });
    });
  }
`);;