HeapSnapshotWorker.AllocationProfile=class{constructor(profile,liveObjectStats){this._strings=profile.strings;this._liveObjectStats=liveObjectStats;this._nextNodeId=1;this._functionInfos=[];this._idToNode={};this._idToTopDownNode={};this._collapsedTopNodeIdToFunctionInfo={};this._traceTops=null;this._buildFunctionAllocationInfos(profile);this._traceTree=this._buildAllocationTree(profile,liveObjectStats);}
_buildFunctionAllocationInfos(profile){var strings=this._strings;var functionInfoFields=profile.snapshot.meta.trace_function_info_fields;var functionNameOffset=functionInfoFields.indexOf('name');var scriptNameOffset=functionInfoFields.indexOf('script_name');var scriptIdOffset=functionInfoFields.indexOf('script_id');var lineOffset=functionInfoFields.indexOf('line');var columnOffset=functionInfoFields.indexOf('column');var functionInfoFieldCount=functionInfoFields.length;var rawInfos=profile.trace_function_infos;var infoLength=rawInfos.length;var functionInfos=this._functionInfos=new Array(infoLength/functionInfoFieldCount);var index=0;for(var i=0;i<infoLength;i+=functionInfoFieldCount){functionInfos[index++]=new HeapSnapshotWorker.FunctionAllocationInfo(strings[rawInfos[i+functionNameOffset]],strings[rawInfos[i+scriptNameOffset]],rawInfos[i+scriptIdOffset],rawInfos[i+lineOffset],rawInfos[i+columnOffset]);}}
_buildAllocationTree(profile,liveObjectStats){var traceTreeRaw=profile.trace_tree;var functionInfos=this._functionInfos;var idToTopDownNode=this._idToTopDownNode;var traceNodeFields=profile.snapshot.meta.trace_node_fields;var nodeIdOffset=traceNodeFields.indexOf('id');var functionInfoIndexOffset=traceNodeFields.indexOf('function_info_index');var allocationCountOffset=traceNodeFields.indexOf('count');var allocationSizeOffset=traceNodeFields.indexOf('size');var childrenOffset=traceNodeFields.indexOf('children');var nodeFieldCount=traceNodeFields.length;function traverseNode(rawNodeArray,nodeOffset,parent){var functionInfo=functionInfos[rawNodeArray[nodeOffset+functionInfoIndexOffset]];var id=rawNodeArray[nodeOffset+nodeIdOffset];var stats=liveObjectStats[id];var liveCount=stats?stats.count:0;var liveSize=stats?stats.size:0;var result=new HeapSnapshotWorker.TopDownAllocationNode(id,functionInfo,rawNodeArray[nodeOffset+allocationCountOffset],rawNodeArray[nodeOffset+allocationSizeOffset],liveCount,liveSize,parent);idToTopDownNode[id]=result;functionInfo.addTraceTopNode(result);var rawChildren=rawNodeArray[nodeOffset+childrenOffset];for(var i=0;i<rawChildren.length;i+=nodeFieldCount)
result.children.push(traverseNode(rawChildren,i,result));return result;}
return traverseNode(traceTreeRaw,0,null);}
serializeTraceTops(){if(this._traceTops)
return this._traceTops;var result=this._traceTops=[];var functionInfos=this._functionInfos;for(var i=0;i<functionInfos.length;i++){var info=functionInfos[i];if(info.totalCount===0)
continue;var nodeId=this._nextNodeId++;var isRoot=i===0;result.push(this._serializeNode(nodeId,info,info.totalCount,info.totalSize,info.totalLiveCount,info.totalLiveSize,!isRoot));this._collapsedTopNodeIdToFunctionInfo[nodeId]=info;}
result.sort(function(a,b){return b.size-a.size;});return result;}
serializeCallers(nodeId){var node=this._ensureBottomUpNode(nodeId);var nodesWithSingleCaller=[];while(node.callers().length===1){node=node.callers()[0];nodesWithSingleCaller.push(this._serializeCaller(node));}
var branchingCallers=[];var callers=node.callers();for(var i=0;i<callers.length;i++)
branchingCallers.push(this._serializeCaller(callers[i]));return new HeapSnapshotModel.AllocationNodeCallers(nodesWithSingleCaller,branchingCallers);}
serializeAllocationStack(traceNodeId){var node=this._idToTopDownNode[traceNodeId];var result=[];while(node){var functionInfo=node.functionInfo;result.push(new HeapSnapshotModel.AllocationStackFrame(functionInfo.functionName,functionInfo.scriptName,functionInfo.scriptId,functionInfo.line,functionInfo.column));node=node.parent;}
return result;}
traceIds(allocationNodeId){return this._ensureBottomUpNode(allocationNodeId).traceTopIds;}
_ensureBottomUpNode(nodeId){var node=this._idToNode[nodeId];if(!node){var functionInfo=this._collapsedTopNodeIdToFunctionInfo[nodeId];node=functionInfo.bottomUpRoot();delete this._collapsedTopNodeIdToFunctionInfo[nodeId];this._idToNode[nodeId]=node;}
return node;}
_serializeCaller(node){var callerId=this._nextNodeId++;this._idToNode[callerId]=node;return this._serializeNode(callerId,node.functionInfo,node.allocationCount,node.allocationSize,node.liveCount,node.liveSize,node.hasCallers());}
_serializeNode(nodeId,functionInfo,count,size,liveCount,liveSize,hasChildren){return new HeapSnapshotModel.SerializedAllocationNode(nodeId,functionInfo.functionName,functionInfo.scriptName,functionInfo.scriptId,functionInfo.line,functionInfo.column,count,size,liveCount,liveSize,hasChildren);}};HeapSnapshotWorker.TopDownAllocationNode=class{constructor(id,functionInfo,count,size,liveCount,liveSize,parent){this.id=id;this.functionInfo=functionInfo;this.allocationCount=count;this.allocationSize=size;this.liveCount=liveCount;this.liveSize=liveSize;this.parent=parent;this.children=[];}};HeapSnapshotWorker.BottomUpAllocationNode=class{constructor(functionInfo){this.functionInfo=functionInfo;this.allocationCount=0;this.allocationSize=0;this.liveCount=0;this.liveSize=0;this.traceTopIds=[];this._callers=[];}
addCaller(traceNode){var functionInfo=traceNode.functionInfo;var result;for(var i=0;i<this._callers.length;i++){var caller=this._callers[i];if(caller.functionInfo===functionInfo){result=caller;break;}}
if(!result){result=new HeapSnapshotWorker.BottomUpAllocationNode(functionInfo);this._callers.push(result);}
return result;}
callers(){return this._callers;}
hasCallers(){return this._callers.length>0;}};HeapSnapshotWorker.FunctionAllocationInfo=class{constructor(functionName,scriptName,scriptId,line,column){this.functionName=functionName;this.scriptName=scriptName;this.scriptId=scriptId;this.line=line;this.column=column;this.totalCount=0;this.totalSize=0;this.totalLiveCount=0;this.totalLiveSize=0;this._traceTops=[];}
addTraceTopNode(node){if(node.allocationCount===0)
return;this._traceTops.push(node);this.totalCount+=node.allocationCount;this.totalSize+=node.allocationSize;this.totalLiveCount+=node.liveCount;this.totalLiveSize+=node.liveSize;}
bottomUpRoot(){if(!this._traceTops.length)
return null;if(!this._bottomUpTree)
this._buildAllocationTraceTree();return this._bottomUpTree;}
_buildAllocationTraceTree(){this._bottomUpTree=new HeapSnapshotWorker.BottomUpAllocationNode(this);for(var i=0;i<this._traceTops.length;i++){var node=this._traceTops[i];var bottomUpNode=this._bottomUpTree;var count=node.allocationCount;var size=node.allocationSize;var liveCount=node.liveCount;var liveSize=node.liveSize;var traceId=node.id;while(true){bottomUpNode.allocationCount+=count;bottomUpNode.allocationSize+=size;bottomUpNode.liveCount+=liveCount;bottomUpNode.liveSize+=liveSize;bottomUpNode.traceTopIds.push(traceId);node=node.parent;if(node===null)
break;bottomUpNode=bottomUpNode.addCaller(node);}}}};;HeapSnapshotWorker.HeapSnapshotItem=function(){};HeapSnapshotWorker.HeapSnapshotItem.prototype={itemIndex(){},serialize(){}};HeapSnapshotWorker.HeapSnapshotEdge=class{constructor(snapshot,edgeIndex){this._snapshot=snapshot;this._edges=snapshot.containmentEdges;this.edgeIndex=edgeIndex||0;}
clone(){return new HeapSnapshotWorker.HeapSnapshotEdge(this._snapshot,this.edgeIndex);}
hasStringName(){throw new Error('Not implemented');}
name(){throw new Error('Not implemented');}
node(){return this._snapshot.createNode(this.nodeIndex());}
nodeIndex(){return this._edges[this.edgeIndex+this._snapshot._edgeToNodeOffset];}
toString(){return'HeapSnapshotEdge: '+this.name();}
type(){return this._snapshot._edgeTypes[this.rawType()];}
itemIndex(){return this.edgeIndex;}
serialize(){return new HeapSnapshotModel.Edge(this.name(),this.node().serialize(),this.type(),this.edgeIndex);}
rawType(){return this._edges[this.edgeIndex+this._snapshot._edgeTypeOffset];}};HeapSnapshotWorker.HeapSnapshotItemIterator=function(){};HeapSnapshotWorker.HeapSnapshotItemIterator.prototype={hasNext(){},item(){},next(){}};HeapSnapshotWorker.HeapSnapshotItemIndexProvider=function(){};HeapSnapshotWorker.HeapSnapshotItemIndexProvider.prototype={itemForIndex(newIndex){},};HeapSnapshotWorker.HeapSnapshotNodeIndexProvider=class{constructor(snapshot){this._node=snapshot.createNode();}
itemForIndex(index){this._node.nodeIndex=index;return this._node;}};HeapSnapshotWorker.HeapSnapshotEdgeIndexProvider=class{constructor(snapshot){this._edge=snapshot.createEdge(0);}
itemForIndex(index){this._edge.edgeIndex=index;return this._edge;}};HeapSnapshotWorker.HeapSnapshotRetainerEdgeIndexProvider=class{constructor(snapshot){this._retainerEdge=snapshot.createRetainingEdge(0);}
itemForIndex(index){this._retainerEdge.setRetainerIndex(index);return this._retainerEdge;}};HeapSnapshotWorker.HeapSnapshotEdgeIterator=class{constructor(node){this._sourceNode=node;this.edge=node._snapshot.createEdge(node.edgeIndexesStart());}
hasNext(){return this.edge.edgeIndex<this._sourceNode.edgeIndexesEnd();}
item(){return this.edge;}
next(){this.edge.edgeIndex+=this.edge._snapshot._edgeFieldsCount;}};HeapSnapshotWorker.HeapSnapshotRetainerEdge=class{constructor(snapshot,retainerIndex){this._snapshot=snapshot;this.setRetainerIndex(retainerIndex);}
clone(){return new HeapSnapshotWorker.HeapSnapshotRetainerEdge(this._snapshot,this.retainerIndex());}
hasStringName(){return this._edge().hasStringName();}
name(){return this._edge().name();}
node(){return this._node();}
nodeIndex(){return this._retainingNodeIndex;}
retainerIndex(){return this._retainerIndex;}
setRetainerIndex(retainerIndex){if(retainerIndex===this._retainerIndex)
return;this._retainerIndex=retainerIndex;this._globalEdgeIndex=this._snapshot._retainingEdges[retainerIndex];this._retainingNodeIndex=this._snapshot._retainingNodes[retainerIndex];this._edgeInstance=null;this._nodeInstance=null;}
set edgeIndex(edgeIndex){this.setRetainerIndex(edgeIndex);}
_node(){if(!this._nodeInstance)
this._nodeInstance=this._snapshot.createNode(this._retainingNodeIndex);return this._nodeInstance;}
_edge(){if(!this._edgeInstance)
this._edgeInstance=this._snapshot.createEdge(this._globalEdgeIndex);return this._edgeInstance;}
toString(){return this._edge().toString();}
itemIndex(){return this._retainerIndex;}
serialize(){return new HeapSnapshotModel.Edge(this.name(),this.node().serialize(),this.type(),this._globalEdgeIndex);}
type(){return this._edge().type();}};HeapSnapshotWorker.HeapSnapshotRetainerEdgeIterator=class{constructor(retainedNode){var snapshot=retainedNode._snapshot;var retainedNodeOrdinal=retainedNode.ordinal();var retainerIndex=snapshot._firstRetainerIndex[retainedNodeOrdinal];this._retainersEnd=snapshot._firstRetainerIndex[retainedNodeOrdinal+1];this.retainer=snapshot.createRetainingEdge(retainerIndex);}
hasNext(){return this.retainer.retainerIndex()<this._retainersEnd;}
item(){return this.retainer;}
next(){this.retainer.setRetainerIndex(this.retainer.retainerIndex()+1);}};HeapSnapshotWorker.HeapSnapshotNode=class{constructor(snapshot,nodeIndex){this._snapshot=snapshot;this.nodeIndex=nodeIndex||0;}
distance(){return this._snapshot._nodeDistances[this.nodeIndex/this._snapshot._nodeFieldCount];}
className(){throw new Error('Not implemented');}
classIndex(){throw new Error('Not implemented');}
dominatorIndex(){var nodeFieldCount=this._snapshot._nodeFieldCount;return this._snapshot._dominatorsTree[this.nodeIndex/this._snapshot._nodeFieldCount]*nodeFieldCount;}
edges(){return new HeapSnapshotWorker.HeapSnapshotEdgeIterator(this);}
edgesCount(){return(this.edgeIndexesEnd()-this.edgeIndexesStart())/this._snapshot._edgeFieldsCount;}
id(){throw new Error('Not implemented');}
isRoot(){return this.nodeIndex===this._snapshot._rootNodeIndex;}
name(){return this._snapshot.strings[this._name()];}
retainedSize(){return this._snapshot._retainedSizes[this.ordinal()];}
retainers(){return new HeapSnapshotWorker.HeapSnapshotRetainerEdgeIterator(this);}
retainersCount(){var snapshot=this._snapshot;var ordinal=this.ordinal();return snapshot._firstRetainerIndex[ordinal+1]-snapshot._firstRetainerIndex[ordinal];}
selfSize(){var snapshot=this._snapshot;return snapshot.nodes[this.nodeIndex+snapshot._nodeSelfSizeOffset];}
type(){return this._snapshot._nodeTypes[this.rawType()];}
traceNodeId(){var snapshot=this._snapshot;return snapshot.nodes[this.nodeIndex+snapshot._nodeTraceNodeIdOffset];}
itemIndex(){return this.nodeIndex;}
serialize(){return new HeapSnapshotModel.Node(this.id(),this.name(),this.distance(),this.nodeIndex,this.retainedSize(),this.selfSize(),this.type());}
_name(){var snapshot=this._snapshot;return snapshot.nodes[this.nodeIndex+snapshot._nodeNameOffset];}
edgeIndexesStart(){return this._snapshot._firstEdgeIndexes[this.ordinal()];}
edgeIndexesEnd(){return this._snapshot._firstEdgeIndexes[this.ordinal()+1];}
ordinal(){return this.nodeIndex/this._snapshot._nodeFieldCount;}
_nextNodeIndex(){return this.nodeIndex+this._snapshot._nodeFieldCount;}
rawType(){var snapshot=this._snapshot;return snapshot.nodes[this.nodeIndex+snapshot._nodeTypeOffset];}};HeapSnapshotWorker.HeapSnapshotNodeIterator=class{constructor(node){this.node=node;this._nodesLength=node._snapshot.nodes.length;}
hasNext(){return this.node.nodeIndex<this._nodesLength;}
item(){return this.node;}
next(){this.node.nodeIndex=this.node._nextNodeIndex();}};HeapSnapshotWorker.HeapSnapshotIndexRangeIterator=class{constructor(itemProvider,indexes){this._itemProvider=itemProvider;this._indexes=indexes;this._position=0;}
hasNext(){return this._position<this._indexes.length;}
item(){var index=this._indexes[this._position];return this._itemProvider.itemForIndex(index);}
next(){++this._position;}};HeapSnapshotWorker.HeapSnapshotFilteredIterator=class{constructor(iterator,filter){this._iterator=iterator;this._filter=filter;this._skipFilteredItems();}
hasNext(){return this._iterator.hasNext();}
item(){return this._iterator.item();}
next(){this._iterator.next();this._skipFilteredItems();}
_skipFilteredItems(){while(this._iterator.hasNext()&&!this._filter(this._iterator.item()))
this._iterator.next();}};HeapSnapshotWorker.HeapSnapshotProgress=class{constructor(dispatcher){this._dispatcher=dispatcher;}
updateStatus(status){this._sendUpdateEvent(Common.UIString(status));}
updateProgress(title,value,total){var percentValue=((total?(value/total):0)*100).toFixed(0);this._sendUpdateEvent(Common.UIString(title,percentValue));}
reportProblem(error){if(this._dispatcher)
this._dispatcher.sendEvent(HeapSnapshotModel.HeapSnapshotProgressEvent.BrokenSnapshot,error);}
_sendUpdateEvent(text){if(this._dispatcher)
this._dispatcher.sendEvent(HeapSnapshotModel.HeapSnapshotProgressEvent.Update,text);}};HeapSnapshotWorker.HeapSnapshotProblemReport=class{constructor(title){this._errors=[title];}
addError(error){if(this._errors.length>100)
return;this._errors.push(error);}
toString(){return this._errors.join('\n  ');}};HeapSnapshotWorker.HeapSnapshot=class{constructor(profile,progress){this.nodes=profile.nodes;this.containmentEdges=profile.edges;this._metaNode=profile.snapshot.meta;this._rawSamples=profile.samples;this._samples=null;this.strings=profile.strings;this._progress=progress;this._noDistance=-5;this._rootNodeIndex=0;if(profile.snapshot.root_index)
this._rootNodeIndex=profile.snapshot.root_index;this._snapshotDiffs={};this._aggregatesForDiff=null;this._aggregates={};this._aggregatesSortedFlags={};this._profile=profile;}
initialize(){var meta=this._metaNode;this._nodeTypeOffset=meta.node_fields.indexOf('type');this._nodeNameOffset=meta.node_fields.indexOf('name');this._nodeIdOffset=meta.node_fields.indexOf('id');this._nodeSelfSizeOffset=meta.node_fields.indexOf('self_size');this._nodeEdgeCountOffset=meta.node_fields.indexOf('edge_count');this._nodeTraceNodeIdOffset=meta.node_fields.indexOf('trace_node_id');this._nodeFieldCount=meta.node_fields.length;this._nodeTypes=meta.node_types[this._nodeTypeOffset];this._nodeArrayType=this._nodeTypes.indexOf('array');this._nodeHiddenType=this._nodeTypes.indexOf('hidden');this._nodeObjectType=this._nodeTypes.indexOf('object');this._nodeNativeType=this._nodeTypes.indexOf('native');this._nodeConsStringType=this._nodeTypes.indexOf('concatenated string');this._nodeSlicedStringType=this._nodeTypes.indexOf('sliced string');this._nodeCodeType=this._nodeTypes.indexOf('code');this._nodeSyntheticType=this._nodeTypes.indexOf('synthetic');this._edgeFieldsCount=meta.edge_fields.length;this._edgeTypeOffset=meta.edge_fields.indexOf('type');this._edgeNameOffset=meta.edge_fields.indexOf('name_or_index');this._edgeToNodeOffset=meta.edge_fields.indexOf('to_node');this._edgeTypes=meta.edge_types[this._edgeTypeOffset];this._edgeTypes.push('invisible');this._edgeElementType=this._edgeTypes.indexOf('element');this._edgeHiddenType=this._edgeTypes.indexOf('hidden');this._edgeInternalType=this._edgeTypes.indexOf('internal');this._edgeShortcutType=this._edgeTypes.indexOf('shortcut');this._edgeWeakType=this._edgeTypes.indexOf('weak');this._edgeInvisibleType=this._edgeTypes.indexOf('invisible');this.nodeCount=this.nodes.length/this._nodeFieldCount;this._edgeCount=this.containmentEdges.length/this._edgeFieldsCount;this._retainedSizes=new Float64Array(this.nodeCount);this._firstEdgeIndexes=new Uint32Array(this.nodeCount+1);this._retainingNodes=new Uint32Array(this._edgeCount);this._retainingEdges=new Uint32Array(this._edgeCount);this._firstRetainerIndex=new Uint32Array(this.nodeCount+1);this._nodeDistances=new Int32Array(this.nodeCount);this._firstDominatedNodeIndex=new Uint32Array(this.nodeCount+1);this._dominatedNodes=new Uint32Array(this.nodeCount-1);this._progress.updateStatus('Building edge indexes\u2026');this._buildEdgeIndexes();this._progress.updateStatus('Building retainers\u2026');this._buildRetainers();this._progress.updateStatus('Calculating node flags\u2026');this.calculateFlags();this._progress.updateStatus('Calculating distances\u2026');this.calculateDistances();this._progress.updateStatus('Building postorder index\u2026');var result=this._buildPostOrderIndex();this._progress.updateStatus('Building dominator tree\u2026');this._dominatorsTree=this._buildDominatorTree(result.postOrderIndex2NodeOrdinal,result.nodeOrdinal2PostOrderIndex);this._progress.updateStatus('Calculating retained sizes\u2026');this._calculateRetainedSizes(result.postOrderIndex2NodeOrdinal);this._progress.updateStatus('Building dominated nodes\u2026');this._buildDominatedNodes();this._progress.updateStatus('Calculating statistics\u2026');this.calculateStatistics();this._progress.updateStatus('Calculating samples\u2026');this._buildSamples();this._progress.updateStatus('Finished processing.');if(this._profile.snapshot.trace_function_count){this._progress.updateStatus('Building allocation statistics\u2026');var nodes=this.nodes;var nodesLength=nodes.length;var nodeFieldCount=this._nodeFieldCount;var node=this.rootNode();var liveObjects={};for(var nodeIndex=0;nodeIndex<nodesLength;nodeIndex+=nodeFieldCount){node.nodeIndex=nodeIndex;var traceNodeId=node.traceNodeId();var stats=liveObjects[traceNodeId];if(!stats)
liveObjects[traceNodeId]=stats={count:0,size:0,ids:[]};stats.count++;stats.size+=node.selfSize();stats.ids.push(node.id());}
this._allocationProfile=new HeapSnapshotWorker.AllocationProfile(this._profile,liveObjects);this._progress.updateStatus('Done');}}
_buildEdgeIndexes(){var nodes=this.nodes;var nodeCount=this.nodeCount;var firstEdgeIndexes=this._firstEdgeIndexes;var nodeFieldCount=this._nodeFieldCount;var edgeFieldsCount=this._edgeFieldsCount;var nodeEdgeCountOffset=this._nodeEdgeCountOffset;firstEdgeIndexes[nodeCount]=this.containmentEdges.length;for(var nodeOrdinal=0,edgeIndex=0;nodeOrdinal<nodeCount;++nodeOrdinal){firstEdgeIndexes[nodeOrdinal]=edgeIndex;edgeIndex+=nodes[nodeOrdinal*nodeFieldCount+nodeEdgeCountOffset]*edgeFieldsCount;}}
_buildRetainers(){var retainingNodes=this._retainingNodes;var retainingEdges=this._retainingEdges;var firstRetainerIndex=this._firstRetainerIndex;var containmentEdges=this.containmentEdges;var edgeFieldsCount=this._edgeFieldsCount;var nodeFieldCount=this._nodeFieldCount;var edgeToNodeOffset=this._edgeToNodeOffset;var firstEdgeIndexes=this._firstEdgeIndexes;var nodeCount=this.nodeCount;for(var toNodeFieldIndex=edgeToNodeOffset,l=containmentEdges.length;toNodeFieldIndex<l;toNodeFieldIndex+=edgeFieldsCount){var toNodeIndex=containmentEdges[toNodeFieldIndex];if(toNodeIndex%nodeFieldCount)
throw new Error('Invalid toNodeIndex '+toNodeIndex);++firstRetainerIndex[toNodeIndex/nodeFieldCount];}
for(var i=0,firstUnusedRetainerSlot=0;i<nodeCount;i++){var retainersCount=firstRetainerIndex[i];firstRetainerIndex[i]=firstUnusedRetainerSlot;retainingNodes[firstUnusedRetainerSlot]=retainersCount;firstUnusedRetainerSlot+=retainersCount;}
firstRetainerIndex[nodeCount]=retainingNodes.length;var nextNodeFirstEdgeIndex=firstEdgeIndexes[0];for(var srcNodeOrdinal=0;srcNodeOrdinal<nodeCount;++srcNodeOrdinal){var firstEdgeIndex=nextNodeFirstEdgeIndex;nextNodeFirstEdgeIndex=firstEdgeIndexes[srcNodeOrdinal+1];var srcNodeIndex=srcNodeOrdinal*nodeFieldCount;for(var edgeIndex=firstEdgeIndex;edgeIndex<nextNodeFirstEdgeIndex;edgeIndex+=edgeFieldsCount){var toNodeIndex=containmentEdges[edgeIndex+edgeToNodeOffset];if(toNodeIndex%nodeFieldCount)
throw new Error('Invalid toNodeIndex '+toNodeIndex);var firstRetainerSlotIndex=firstRetainerIndex[toNodeIndex/nodeFieldCount];var nextUnusedRetainerSlotIndex=firstRetainerSlotIndex+(--retainingNodes[firstRetainerSlotIndex]);retainingNodes[nextUnusedRetainerSlotIndex]=srcNodeIndex;retainingEdges[nextUnusedRetainerSlotIndex]=edgeIndex;}}}
createNode(nodeIndex){throw new Error('Not implemented');}
createEdge(edgeIndex){throw new Error('Not implemented');}
createRetainingEdge(retainerIndex){throw new Error('Not implemented');}
_allNodes(){return new HeapSnapshotWorker.HeapSnapshotNodeIterator(this.rootNode());}
rootNode(){return this.createNode(this._rootNodeIndex);}
get rootNodeIndex(){return this._rootNodeIndex;}
get totalSize(){return this.rootNode().retainedSize();}
_getDominatedIndex(nodeIndex){if(nodeIndex%this._nodeFieldCount)
throw new Error('Invalid nodeIndex: '+nodeIndex);return this._firstDominatedNodeIndex[nodeIndex/this._nodeFieldCount];}
_createFilter(nodeFilter){var minNodeId=nodeFilter.minNodeId;var maxNodeId=nodeFilter.maxNodeId;var allocationNodeId=nodeFilter.allocationNodeId;var filter;if(typeof allocationNodeId==='number'){filter=this._createAllocationStackFilter(allocationNodeId);filter.key='AllocationNodeId: '+allocationNodeId;}else if(typeof minNodeId==='number'&&typeof maxNodeId==='number'){filter=this._createNodeIdFilter(minNodeId,maxNodeId);filter.key='NodeIdRange: '+minNodeId+'..'+maxNodeId;}
return filter;}
search(searchConfig,nodeFilter){var query=searchConfig.query;function filterString(matchedStringIndexes,string,index){if(string.indexOf(query)!==-1)
matchedStringIndexes.add(index);return matchedStringIndexes;}
var regexp=searchConfig.isRegex?new RegExp(query):createPlainTextSearchRegex(query,'i');function filterRegexp(matchedStringIndexes,string,index){if(regexp.test(string))
matchedStringIndexes.add(index);return matchedStringIndexes;}
var stringFilter=(searchConfig.isRegex||!searchConfig.caseSensitive)?filterRegexp:filterString;var stringIndexes=this.strings.reduce(stringFilter,new Set());if(!stringIndexes.size)
return[];var filter=this._createFilter(nodeFilter);var nodeIds=[];var nodesLength=this.nodes.length;var nodes=this.nodes;var nodeNameOffset=this._nodeNameOffset;var nodeIdOffset=this._nodeIdOffset;var nodeFieldCount=this._nodeFieldCount;var node=this.rootNode();for(var nodeIndex=0;nodeIndex<nodesLength;nodeIndex+=nodeFieldCount){node.nodeIndex=nodeIndex;if(filter&&!filter(node))
continue;if(stringIndexes.has(nodes[nodeIndex+nodeNameOffset]))
nodeIds.push(nodes[nodeIndex+nodeIdOffset]);}
return nodeIds;}
aggregatesWithFilter(nodeFilter){var filter=this._createFilter(nodeFilter);var key=filter?filter.key:'allObjects';return this.aggregates(false,key,filter);}
_createNodeIdFilter(minNodeId,maxNodeId){function nodeIdFilter(node){var id=node.id();return id>minNodeId&&id<=maxNodeId;}
return nodeIdFilter;}
_createAllocationStackFilter(bottomUpAllocationNodeId){var traceIds=this._allocationProfile.traceIds(bottomUpAllocationNodeId);if(!traceIds.length)
return undefined;var set={};for(var i=0;i<traceIds.length;i++)
set[traceIds[i]]=true;function traceIdFilter(node){return!!set[node.traceNodeId()];}
return traceIdFilter;}
aggregates(sortedIndexes,key,filter){var aggregatesByClassName=key&&this._aggregates[key];if(!aggregatesByClassName){var aggregates=this._buildAggregates(filter);this._calculateClassesRetainedSize(aggregates.aggregatesByClassIndex,filter);aggregatesByClassName=aggregates.aggregatesByClassName;if(key)
this._aggregates[key]=aggregatesByClassName;}
if(sortedIndexes&&(!key||!this._aggregatesSortedFlags[key])){this._sortAggregateIndexes(aggregatesByClassName);if(key)
this._aggregatesSortedFlags[key]=sortedIndexes;}
return aggregatesByClassName;}
allocationTracesTops(){return this._allocationProfile.serializeTraceTops();}
allocationNodeCallers(nodeId){return this._allocationProfile.serializeCallers(nodeId);}
allocationStack(nodeIndex){var node=this.createNode(nodeIndex);var allocationNodeId=node.traceNodeId();if(!allocationNodeId)
return null;return this._allocationProfile.serializeAllocationStack(allocationNodeId);}
aggregatesForDiff(){if(this._aggregatesForDiff)
return this._aggregatesForDiff;var aggregatesByClassName=this.aggregates(true,'allObjects');this._aggregatesForDiff={};var node=this.createNode();for(var className in aggregatesByClassName){var aggregate=aggregatesByClassName[className];var indexes=aggregate.idxs;var ids=new Array(indexes.length);var selfSizes=new Array(indexes.length);for(var i=0;i<indexes.length;i++){node.nodeIndex=indexes[i];ids[i]=node.id();selfSizes[i]=node.selfSize();}
this._aggregatesForDiff[className]={indexes:indexes,ids:ids,selfSizes:selfSizes};}
return this._aggregatesForDiff;}
isUserRoot(node){return true;}
forEachRoot(action,userRootsOnly){for(var iter=this.rootNode().edges();iter.hasNext();iter.next()){var node=iter.edge.node();if(!userRootsOnly||this.isUserRoot(node))
action(node);}}
calculateDistances(filter){var nodeCount=this.nodeCount;var distances=this._nodeDistances;var noDistance=this._noDistance;for(var i=0;i<nodeCount;++i)
distances[i]=noDistance;var nodesToVisit=new Uint32Array(this.nodeCount);var nodesToVisitLength=0;function enqueueNode(distance,node){var ordinal=node.ordinal();if(distances[ordinal]!==noDistance)
return;distances[ordinal]=distance;nodesToVisit[nodesToVisitLength++]=node.nodeIndex;}
this.forEachRoot(enqueueNode.bind(null,1),true);this._bfs(nodesToVisit,nodesToVisitLength,distances,filter);nodesToVisitLength=0;this.forEachRoot(enqueueNode.bind(null,HeapSnapshotModel.baseSystemDistance),false);this._bfs(nodesToVisit,nodesToVisitLength,distances,filter);}
_bfs(nodesToVisit,nodesToVisitLength,distances,filter){var edgeFieldsCount=this._edgeFieldsCount;var nodeFieldCount=this._nodeFieldCount;var containmentEdges=this.containmentEdges;var firstEdgeIndexes=this._firstEdgeIndexes;var edgeToNodeOffset=this._edgeToNodeOffset;var edgeTypeOffset=this._edgeTypeOffset;var nodeCount=this.nodeCount;var edgeWeakType=this._edgeWeakType;var noDistance=this._noDistance;var index=0;var edge=this.createEdge(0);var node=this.createNode(0);while(index<nodesToVisitLength){var nodeIndex=nodesToVisit[index++];var nodeOrdinal=nodeIndex/nodeFieldCount;var distance=distances[nodeOrdinal]+1;var firstEdgeIndex=firstEdgeIndexes[nodeOrdinal];var edgesEnd=firstEdgeIndexes[nodeOrdinal+1];node.nodeIndex=nodeIndex;for(var edgeIndex=firstEdgeIndex;edgeIndex<edgesEnd;edgeIndex+=edgeFieldsCount){var edgeType=containmentEdges[edgeIndex+edgeTypeOffset];if(edgeType===edgeWeakType)
continue;var childNodeIndex=containmentEdges[edgeIndex+edgeToNodeOffset];var childNodeOrdinal=childNodeIndex/nodeFieldCount;if(distances[childNodeOrdinal]!==noDistance)
continue;edge.edgeIndex=edgeIndex;if(filter&&!filter(node,edge))
continue;distances[childNodeOrdinal]=distance;nodesToVisit[nodesToVisitLength++]=childNodeIndex;}}
if(nodesToVisitLength>nodeCount){throw new Error('BFS failed. Nodes to visit ('+nodesToVisitLength+') is more than nodes count ('+nodeCount+')');}}
_buildAggregates(filter){var aggregates={};var aggregatesByClassName={};var classIndexes=[];var nodes=this.nodes;var nodesLength=nodes.length;var nodeNativeType=this._nodeNativeType;var nodeFieldCount=this._nodeFieldCount;var selfSizeOffset=this._nodeSelfSizeOffset;var nodeTypeOffset=this._nodeTypeOffset;var node=this.rootNode();var nodeDistances=this._nodeDistances;for(var nodeIndex=0;nodeIndex<nodesLength;nodeIndex+=nodeFieldCount){node.nodeIndex=nodeIndex;if(filter&&!filter(node))
continue;var selfSize=nodes[nodeIndex+selfSizeOffset];if(!selfSize&&nodes[nodeIndex+nodeTypeOffset]!==nodeNativeType)
continue;var classIndex=node.classIndex();var nodeOrdinal=nodeIndex/nodeFieldCount;var distance=nodeDistances[nodeOrdinal];if(!(classIndex in aggregates)){var nodeType=node.type();var nameMatters=nodeType==='object'||nodeType==='native';var value={count:1,distance:distance,self:selfSize,maxRet:0,type:nodeType,name:nameMatters?node.name():null,idxs:[nodeIndex]};aggregates[classIndex]=value;classIndexes.push(classIndex);aggregatesByClassName[node.className()]=value;}else{var clss=aggregates[classIndex];clss.distance=Math.min(clss.distance,distance);++clss.count;clss.self+=selfSize;clss.idxs.push(nodeIndex);}}
for(var i=0,l=classIndexes.length;i<l;++i){var classIndex=classIndexes[i];aggregates[classIndex].idxs=aggregates[classIndex].idxs.slice();}
return{aggregatesByClassName:aggregatesByClassName,aggregatesByClassIndex:aggregates};}
_calculateClassesRetainedSize(aggregates,filter){var rootNodeIndex=this._rootNodeIndex;var node=this.createNode(rootNodeIndex);var list=[rootNodeIndex];var sizes=[-1];var classes=[];var seenClassNameIndexes={};var nodeFieldCount=this._nodeFieldCount;var nodeTypeOffset=this._nodeTypeOffset;var nodeNativeType=this._nodeNativeType;var dominatedNodes=this._dominatedNodes;var nodes=this.nodes;var firstDominatedNodeIndex=this._firstDominatedNodeIndex;while(list.length){var nodeIndex=list.pop();node.nodeIndex=nodeIndex;var classIndex=node.classIndex();var seen=!!seenClassNameIndexes[classIndex];var nodeOrdinal=nodeIndex/nodeFieldCount;var dominatedIndexFrom=firstDominatedNodeIndex[nodeOrdinal];var dominatedIndexTo=firstDominatedNodeIndex[nodeOrdinal+1];if(!seen&&(!filter||filter(node))&&(node.selfSize()||nodes[nodeIndex+nodeTypeOffset]===nodeNativeType)){aggregates[classIndex].maxRet+=node.retainedSize();if(dominatedIndexFrom!==dominatedIndexTo){seenClassNameIndexes[classIndex]=true;sizes.push(list.length);classes.push(classIndex);}}
for(var i=dominatedIndexFrom;i<dominatedIndexTo;i++)
list.push(dominatedNodes[i]);var l=list.length;while(sizes[sizes.length-1]===l){sizes.pop();classIndex=classes.pop();seenClassNameIndexes[classIndex]=false;}}}
_sortAggregateIndexes(aggregates){var nodeA=this.createNode();var nodeB=this.createNode();for(var clss in aggregates){aggregates[clss].idxs.sort((idxA,idxB)=>{nodeA.nodeIndex=idxA;nodeB.nodeIndex=idxB;return nodeA.id()<nodeB.id()?-1:1;});}}
_isEssentialEdge(nodeIndex,edgeType){return edgeType!==this._edgeWeakType&&(edgeType!==this._edgeShortcutType||nodeIndex===this._rootNodeIndex);}
_buildPostOrderIndex(){var nodeFieldCount=this._nodeFieldCount;var nodeCount=this.nodeCount;var rootNodeOrdinal=this._rootNodeIndex/nodeFieldCount;var edgeFieldsCount=this._edgeFieldsCount;var edgeTypeOffset=this._edgeTypeOffset;var edgeToNodeOffset=this._edgeToNodeOffset;var firstEdgeIndexes=this._firstEdgeIndexes;var containmentEdges=this.containmentEdges;var mapAndFlag=this.userObjectsMapAndFlag();var flags=mapAndFlag?mapAndFlag.map:null;var flag=mapAndFlag?mapAndFlag.flag:0;var stackNodes=new Uint32Array(nodeCount);var stackCurrentEdge=new Uint32Array(nodeCount);var postOrderIndex2NodeOrdinal=new Uint32Array(nodeCount);var nodeOrdinal2PostOrderIndex=new Uint32Array(nodeCount);var visited=new Uint8Array(nodeCount);var postOrderIndex=0;var stackTop=0;stackNodes[0]=rootNodeOrdinal;stackCurrentEdge[0]=firstEdgeIndexes[rootNodeOrdinal];visited[rootNodeOrdinal]=1;var iteration=0;while(true){++iteration;while(stackTop>=0){var nodeOrdinal=stackNodes[stackTop];var edgeIndex=stackCurrentEdge[stackTop];var edgesEnd=firstEdgeIndexes[nodeOrdinal+1];if(edgeIndex<edgesEnd){stackCurrentEdge[stackTop]+=edgeFieldsCount;var edgeType=containmentEdges[edgeIndex+edgeTypeOffset];if(!this._isEssentialEdge(nodeOrdinal*nodeFieldCount,edgeType))
continue;var childNodeIndex=containmentEdges[edgeIndex+edgeToNodeOffset];var childNodeOrdinal=childNodeIndex/nodeFieldCount;if(visited[childNodeOrdinal])
continue;var nodeFlag=!flags||(flags[nodeOrdinal]&flag);var childNodeFlag=!flags||(flags[childNodeOrdinal]&flag);if(nodeOrdinal!==rootNodeOrdinal&&childNodeFlag&&!nodeFlag)
continue;++stackTop;stackNodes[stackTop]=childNodeOrdinal;stackCurrentEdge[stackTop]=firstEdgeIndexes[childNodeOrdinal];visited[childNodeOrdinal]=1;}else{nodeOrdinal2PostOrderIndex[nodeOrdinal]=postOrderIndex;postOrderIndex2NodeOrdinal[postOrderIndex++]=nodeOrdinal;--stackTop;}}
if(postOrderIndex===nodeCount||iteration>1)
break;var errors=new HeapSnapshotWorker.HeapSnapshotProblemReport(`Heap snapshot: ${nodeCount -
          postOrderIndex} nodes are unreachable from the root. Following nodes have only weak retainers:`);var dumpNode=this.rootNode();--postOrderIndex;stackTop=0;stackNodes[0]=rootNodeOrdinal;stackCurrentEdge[0]=firstEdgeIndexes[rootNodeOrdinal+1];for(var i=0;i<nodeCount;++i){if(visited[i]||!this._hasOnlyWeakRetainers(i))
continue;stackNodes[++stackTop]=i;stackCurrentEdge[stackTop]=firstEdgeIndexes[i];visited[i]=1;dumpNode.nodeIndex=i*nodeFieldCount;var retainers=[];for(var it=dumpNode.retainers();it.hasNext();it.next())
retainers.push(`${it.item().node().name()}@${it.item().node().id()}.${it.item().name()}`);errors.addError(`${dumpNode.name()} @${dumpNode.id()}  weak retainers: ${retainers.join(', ')}`);}
console.warn(errors.toString());}
if(postOrderIndex!==nodeCount){var errors=new HeapSnapshotWorker.HeapSnapshotProblemReport('Still found '+(nodeCount-postOrderIndex)+' unreachable nodes in heap snapshot:');var dumpNode=this.rootNode();--postOrderIndex;for(var i=0;i<nodeCount;++i){if(visited[i])
continue;dumpNode.nodeIndex=i*nodeFieldCount;errors.addError(dumpNode.name()+' @'+dumpNode.id());nodeOrdinal2PostOrderIndex[i]=postOrderIndex;postOrderIndex2NodeOrdinal[postOrderIndex++]=i;}
nodeOrdinal2PostOrderIndex[rootNodeOrdinal]=postOrderIndex;postOrderIndex2NodeOrdinal[postOrderIndex++]=rootNodeOrdinal;console.warn(errors.toString());}
return{postOrderIndex2NodeOrdinal:postOrderIndex2NodeOrdinal,nodeOrdinal2PostOrderIndex:nodeOrdinal2PostOrderIndex};}
_hasOnlyWeakRetainers(nodeOrdinal){var edgeTypeOffset=this._edgeTypeOffset;var edgeWeakType=this._edgeWeakType;var edgeShortcutType=this._edgeShortcutType;var containmentEdges=this.containmentEdges;var retainingEdges=this._retainingEdges;var beginRetainerIndex=this._firstRetainerIndex[nodeOrdinal];var endRetainerIndex=this._firstRetainerIndex[nodeOrdinal+1];for(var retainerIndex=beginRetainerIndex;retainerIndex<endRetainerIndex;++retainerIndex){var retainerEdgeIndex=retainingEdges[retainerIndex];var retainerEdgeType=containmentEdges[retainerEdgeIndex+edgeTypeOffset];if(retainerEdgeType!==edgeWeakType&&retainerEdgeType!==edgeShortcutType)
return false;}
return true;}
_buildDominatorTree(postOrderIndex2NodeOrdinal,nodeOrdinal2PostOrderIndex){var nodeFieldCount=this._nodeFieldCount;var firstRetainerIndex=this._firstRetainerIndex;var retainingNodes=this._retainingNodes;var retainingEdges=this._retainingEdges;var edgeFieldsCount=this._edgeFieldsCount;var edgeTypeOffset=this._edgeTypeOffset;var edgeToNodeOffset=this._edgeToNodeOffset;var firstEdgeIndexes=this._firstEdgeIndexes;var containmentEdges=this.containmentEdges;var rootNodeIndex=this._rootNodeIndex;var mapAndFlag=this.userObjectsMapAndFlag();var flags=mapAndFlag?mapAndFlag.map:null;var flag=mapAndFlag?mapAndFlag.flag:0;var nodesCount=postOrderIndex2NodeOrdinal.length;var rootPostOrderedIndex=nodesCount-1;var noEntry=nodesCount;var dominators=new Uint32Array(nodesCount);for(var i=0;i<rootPostOrderedIndex;++i)
dominators[i]=noEntry;dominators[rootPostOrderedIndex]=rootPostOrderedIndex;var affected=new Uint8Array(nodesCount);var nodeOrdinal;{nodeOrdinal=this._rootNodeIndex/nodeFieldCount;var endEdgeIndex=firstEdgeIndexes[nodeOrdinal+1];for(var edgeIndex=firstEdgeIndexes[nodeOrdinal];edgeIndex<endEdgeIndex;edgeIndex+=edgeFieldsCount){var edgeType=containmentEdges[edgeIndex+edgeTypeOffset];if(!this._isEssentialEdge(this._rootNodeIndex,edgeType))
continue;var childNodeOrdinal=containmentEdges[edgeIndex+edgeToNodeOffset]/nodeFieldCount;affected[nodeOrdinal2PostOrderIndex[childNodeOrdinal]]=1;}}
var changed=true;while(changed){changed=false;for(var postOrderIndex=rootPostOrderedIndex-1;postOrderIndex>=0;--postOrderIndex){if(affected[postOrderIndex]===0)
continue;affected[postOrderIndex]=0;if(dominators[postOrderIndex]===rootPostOrderedIndex)
continue;nodeOrdinal=postOrderIndex2NodeOrdinal[postOrderIndex];var nodeFlag=!flags||(flags[nodeOrdinal]&flag);var newDominatorIndex=noEntry;var beginRetainerIndex=firstRetainerIndex[nodeOrdinal];var endRetainerIndex=firstRetainerIndex[nodeOrdinal+1];var orphanNode=true;for(var retainerIndex=beginRetainerIndex;retainerIndex<endRetainerIndex;++retainerIndex){var retainerEdgeIndex=retainingEdges[retainerIndex];var retainerEdgeType=containmentEdges[retainerEdgeIndex+edgeTypeOffset];var retainerNodeIndex=retainingNodes[retainerIndex];if(!this._isEssentialEdge(retainerNodeIndex,retainerEdgeType))
continue;orphanNode=false;var retainerNodeOrdinal=retainerNodeIndex/nodeFieldCount;var retainerNodeFlag=!flags||(flags[retainerNodeOrdinal]&flag);if(retainerNodeIndex!==rootNodeIndex&&nodeFlag&&!retainerNodeFlag)
continue;var retanerPostOrderIndex=nodeOrdinal2PostOrderIndex[retainerNodeOrdinal];if(dominators[retanerPostOrderIndex]!==noEntry){if(newDominatorIndex===noEntry){newDominatorIndex=retanerPostOrderIndex;}else{while(retanerPostOrderIndex!==newDominatorIndex){while(retanerPostOrderIndex<newDominatorIndex)
retanerPostOrderIndex=dominators[retanerPostOrderIndex];while(newDominatorIndex<retanerPostOrderIndex)
newDominatorIndex=dominators[newDominatorIndex];}}
if(newDominatorIndex===rootPostOrderedIndex)
break;}}
if(orphanNode)
newDominatorIndex=rootPostOrderedIndex;if(newDominatorIndex!==noEntry&&dominators[postOrderIndex]!==newDominatorIndex){dominators[postOrderIndex]=newDominatorIndex;changed=true;nodeOrdinal=postOrderIndex2NodeOrdinal[postOrderIndex];var beginEdgeToNodeFieldIndex=firstEdgeIndexes[nodeOrdinal]+edgeToNodeOffset;var endEdgeToNodeFieldIndex=firstEdgeIndexes[nodeOrdinal+1];for(var toNodeFieldIndex=beginEdgeToNodeFieldIndex;toNodeFieldIndex<endEdgeToNodeFieldIndex;toNodeFieldIndex+=edgeFieldsCount){var childNodeOrdinal=containmentEdges[toNodeFieldIndex]/nodeFieldCount;affected[nodeOrdinal2PostOrderIndex[childNodeOrdinal]]=1;}}}}
var dominatorsTree=new Uint32Array(nodesCount);for(var postOrderIndex=0,l=dominators.length;postOrderIndex<l;++postOrderIndex){nodeOrdinal=postOrderIndex2NodeOrdinal[postOrderIndex];dominatorsTree[nodeOrdinal]=postOrderIndex2NodeOrdinal[dominators[postOrderIndex]];}
return dominatorsTree;}
_calculateRetainedSizes(postOrderIndex2NodeOrdinal){var nodeCount=this.nodeCount;var nodes=this.nodes;var nodeSelfSizeOffset=this._nodeSelfSizeOffset;var nodeFieldCount=this._nodeFieldCount;var dominatorsTree=this._dominatorsTree;var retainedSizes=this._retainedSizes;for(var nodeOrdinal=0;nodeOrdinal<nodeCount;++nodeOrdinal)
retainedSizes[nodeOrdinal]=nodes[nodeOrdinal*nodeFieldCount+nodeSelfSizeOffset];for(var postOrderIndex=0;postOrderIndex<nodeCount-1;++postOrderIndex){var nodeOrdinal=postOrderIndex2NodeOrdinal[postOrderIndex];var dominatorOrdinal=dominatorsTree[nodeOrdinal];retainedSizes[dominatorOrdinal]+=retainedSizes[nodeOrdinal];}}
_buildDominatedNodes(){var indexArray=this._firstDominatedNodeIndex;var dominatedNodes=this._dominatedNodes;var nodeFieldCount=this._nodeFieldCount;var dominatorsTree=this._dominatorsTree;var fromNodeOrdinal=0;var toNodeOrdinal=this.nodeCount;var rootNodeOrdinal=this._rootNodeIndex/nodeFieldCount;if(rootNodeOrdinal===fromNodeOrdinal)
fromNodeOrdinal=1;else if(rootNodeOrdinal===toNodeOrdinal-1)
toNodeOrdinal=toNodeOrdinal-1;else
throw new Error('Root node is expected to be either first or last');for(var nodeOrdinal=fromNodeOrdinal;nodeOrdinal<toNodeOrdinal;++nodeOrdinal)
++indexArray[dominatorsTree[nodeOrdinal]];var firstDominatedNodeIndex=0;for(var i=0,l=this.nodeCount;i<l;++i){var dominatedCount=dominatedNodes[firstDominatedNodeIndex]=indexArray[i];indexArray[i]=firstDominatedNodeIndex;firstDominatedNodeIndex+=dominatedCount;}
indexArray[this.nodeCount]=dominatedNodes.length;for(var nodeOrdinal=fromNodeOrdinal;nodeOrdinal<toNodeOrdinal;++nodeOrdinal){var dominatorOrdinal=dominatorsTree[nodeOrdinal];var dominatedRefIndex=indexArray[dominatorOrdinal];dominatedRefIndex+=(--dominatedNodes[dominatedRefIndex]);dominatedNodes[dominatedRefIndex]=nodeOrdinal*nodeFieldCount;}}
_buildSamples(){var samples=this._rawSamples;if(!samples||!samples.length)
return;var sampleCount=samples.length/2;var sizeForRange=new Array(sampleCount);var timestamps=new Array(sampleCount);var lastAssignedIds=new Array(sampleCount);var timestampOffset=this._metaNode.sample_fields.indexOf('timestamp_us');var lastAssignedIdOffset=this._metaNode.sample_fields.indexOf('last_assigned_id');for(var i=0;i<sampleCount;i++){sizeForRange[i]=0;timestamps[i]=(samples[2*i+timestampOffset])/1000;lastAssignedIds[i]=samples[2*i+lastAssignedIdOffset];}
var nodes=this.nodes;var nodesLength=nodes.length;var nodeFieldCount=this._nodeFieldCount;var node=this.rootNode();for(var nodeIndex=0;nodeIndex<nodesLength;nodeIndex+=nodeFieldCount){node.nodeIndex=nodeIndex;var nodeId=node.id();if(nodeId%2===0)
continue;var rangeIndex=lastAssignedIds.lowerBound(nodeId);if(rangeIndex===sampleCount){continue;}
sizeForRange[rangeIndex]+=node.selfSize();}
this._samples=new HeapSnapshotModel.Samples(timestamps,lastAssignedIds,sizeForRange);}
getSamples(){return this._samples;}
calculateFlags(){throw new Error('Not implemented');}
calculateStatistics(){throw new Error('Not implemented');}
userObjectsMapAndFlag(){throw new Error('Not implemented');}
calculateSnapshotDiff(baseSnapshotId,baseSnapshotAggregates){var snapshotDiff=this._snapshotDiffs[baseSnapshotId];if(snapshotDiff)
return snapshotDiff;snapshotDiff={};var aggregates=this.aggregates(true,'allObjects');for(var className in baseSnapshotAggregates){var baseAggregate=baseSnapshotAggregates[className];var diff=this._calculateDiffForClass(baseAggregate,aggregates[className]);if(diff)
snapshotDiff[className]=diff;}
var emptyBaseAggregate=new HeapSnapshotModel.AggregateForDiff();for(var className in aggregates){if(className in baseSnapshotAggregates)
continue;snapshotDiff[className]=this._calculateDiffForClass(emptyBaseAggregate,aggregates[className]);}
this._snapshotDiffs[baseSnapshotId]=snapshotDiff;return snapshotDiff;}
_calculateDiffForClass(baseAggregate,aggregate){var baseIds=baseAggregate.ids;var baseIndexes=baseAggregate.indexes;var baseSelfSizes=baseAggregate.selfSizes;var indexes=aggregate?aggregate.idxs:[];var i=0,l=baseIds.length;var j=0,m=indexes.length;var diff=new HeapSnapshotModel.Diff();var nodeB=this.createNode(indexes[j]);while(i<l&&j<m){var nodeAId=baseIds[i];if(nodeAId<nodeB.id()){diff.deletedIndexes.push(baseIndexes[i]);diff.removedCount++;diff.removedSize+=baseSelfSizes[i];++i;}else if(nodeAId>nodeB.id()){diff.addedIndexes.push(indexes[j]);diff.addedCount++;diff.addedSize+=nodeB.selfSize();nodeB.nodeIndex=indexes[++j];}else{++i;nodeB.nodeIndex=indexes[++j];}}
while(i<l){diff.deletedIndexes.push(baseIndexes[i]);diff.removedCount++;diff.removedSize+=baseSelfSizes[i];++i;}
while(j<m){diff.addedIndexes.push(indexes[j]);diff.addedCount++;diff.addedSize+=nodeB.selfSize();nodeB.nodeIndex=indexes[++j];}
diff.countDelta=diff.addedCount-diff.removedCount;diff.sizeDelta=diff.addedSize-diff.removedSize;if(!diff.addedCount&&!diff.removedCount)
return null;return diff;}
_nodeForSnapshotObjectId(snapshotObjectId){for(var it=this._allNodes();it.hasNext();it.next()){if(it.node.id()===snapshotObjectId)
return it.node;}
return null;}
nodeClassName(snapshotObjectId){var node=this._nodeForSnapshotObjectId(snapshotObjectId);if(node)
return node.className();return null;}
idsOfObjectsWithName(name){var ids=[];for(var it=this._allNodes();it.hasNext();it.next()){if(it.item().name()===name)
ids.push(it.item().id());}
return ids;}
createEdgesProvider(nodeIndex){var node=this.createNode(nodeIndex);var filter=this.containmentEdgesFilter();var indexProvider=new HeapSnapshotWorker.HeapSnapshotEdgeIndexProvider(this);return new HeapSnapshotWorker.HeapSnapshotEdgesProvider(this,filter,node.edges(),indexProvider);}
createEdgesProviderForTest(nodeIndex,filter){var node=this.createNode(nodeIndex);var indexProvider=new HeapSnapshotWorker.HeapSnapshotEdgeIndexProvider(this);return new HeapSnapshotWorker.HeapSnapshotEdgesProvider(this,filter,node.edges(),indexProvider);}
retainingEdgesFilter(){return null;}
containmentEdgesFilter(){return null;}
createRetainingEdgesProvider(nodeIndex){var node=this.createNode(nodeIndex);var filter=this.retainingEdgesFilter();var indexProvider=new HeapSnapshotWorker.HeapSnapshotRetainerEdgeIndexProvider(this);return new HeapSnapshotWorker.HeapSnapshotEdgesProvider(this,filter,node.retainers(),indexProvider);}
createAddedNodesProvider(baseSnapshotId,className){var snapshotDiff=this._snapshotDiffs[baseSnapshotId];var diffForClass=snapshotDiff[className];return new HeapSnapshotWorker.HeapSnapshotNodesProvider(this,diffForClass.addedIndexes);}
createDeletedNodesProvider(nodeIndexes){return new HeapSnapshotWorker.HeapSnapshotNodesProvider(this,nodeIndexes);}
createNodesProviderForClass(className,nodeFilter){return new HeapSnapshotWorker.HeapSnapshotNodesProvider(this,this.aggregatesWithFilter(nodeFilter)[className].idxs);}
_maxJsNodeId(){var nodeFieldCount=this._nodeFieldCount;var nodes=this.nodes;var nodesLength=nodes.length;var id=0;for(var nodeIndex=this._nodeIdOffset;nodeIndex<nodesLength;nodeIndex+=nodeFieldCount){var nextId=nodes[nodeIndex];if(nextId%2===0)
continue;if(id<nextId)
id=nextId;}
return id;}
updateStaticData(){return new HeapSnapshotModel.StaticData(this.nodeCount,this._rootNodeIndex,this.totalSize,this._maxJsNodeId());}};HeapSnapshotWorker.HeapSnapshot.AggregatedInfo;var HeapSnapshotMetainfo=class{constructor(){this.node_fields=[];this.node_types=[];this.edge_fields=[];this.edge_types=[];this.trace_function_info_fields=[];this.trace_node_fields=[];this.sample_fields=[];this.type_strings={};}};var HeapSnapshotHeader=class{constructor(){this.title='';this.meta=new HeapSnapshotMetainfo();this.node_count=0;this.edge_count=0;this.trace_function_count=0;}};HeapSnapshotWorker.HeapSnapshotItemProvider=class{constructor(iterator,indexProvider){this._iterator=iterator;this._indexProvider=indexProvider;this._isEmpty=!iterator.hasNext();this._iterationOrder=null;this._currentComparator=null;this._sortedPrefixLength=0;this._sortedSuffixLength=0;}
_createIterationOrder(){if(this._iterationOrder)
return;this._iterationOrder=[];for(var iterator=this._iterator;iterator.hasNext();iterator.next())
this._iterationOrder.push(iterator.item().itemIndex());}
isEmpty(){return this._isEmpty;}
serializeItemsRange(begin,end){this._createIterationOrder();if(begin>end)
throw new Error('Start position > end position: '+begin+' > '+end);if(end>this._iterationOrder.length)
end=this._iterationOrder.length;if(this._sortedPrefixLength<end&&begin<this._iterationOrder.length-this._sortedSuffixLength){this.sort(this._currentComparator,this._sortedPrefixLength,this._iterationOrder.length-1-this._sortedSuffixLength,begin,end-1);if(begin<=this._sortedPrefixLength)
this._sortedPrefixLength=end;if(end>=this._iterationOrder.length-this._sortedSuffixLength)
this._sortedSuffixLength=this._iterationOrder.length-begin;}
var position=begin;var count=end-begin;var result=new Array(count);for(var i=0;i<count;++i){var itemIndex=this._iterationOrder[position++];var item=this._indexProvider.itemForIndex(itemIndex);result[i]=item.serialize();}
return new HeapSnapshotModel.ItemsRange(begin,end,this._iterationOrder.length,result);}
sortAndRewind(comparator){this._currentComparator=comparator;this._sortedPrefixLength=0;this._sortedSuffixLength=0;}};HeapSnapshotWorker.HeapSnapshotEdgesProvider=class extends HeapSnapshotWorker.HeapSnapshotItemProvider{constructor(snapshot,filter,edgesIter,indexProvider){var iter=filter?new HeapSnapshotWorker.HeapSnapshotFilteredIterator(edgesIter,(filter)):edgesIter;super(iter,indexProvider);this.snapshot=snapshot;}
sort(comparator,leftBound,rightBound,windowLeft,windowRight){var fieldName1=comparator.fieldName1;var fieldName2=comparator.fieldName2;var ascending1=comparator.ascending1;var ascending2=comparator.ascending2;var edgeA=this._iterator.item().clone();var edgeB=edgeA.clone();var nodeA=this.snapshot.createNode();var nodeB=this.snapshot.createNode();function compareEdgeFieldName(ascending,indexA,indexB){edgeA.edgeIndex=indexA;edgeB.edgeIndex=indexB;if(edgeB.name()==='__proto__')
return-1;if(edgeA.name()==='__proto__')
return 1;var result=edgeA.hasStringName()===edgeB.hasStringName()?(edgeA.name()<edgeB.name()?-1:(edgeA.name()>edgeB.name()?1:0)):(edgeA.hasStringName()?-1:1);return ascending?result:-result;}
function compareNodeField(fieldName,ascending,indexA,indexB){edgeA.edgeIndex=indexA;nodeA.nodeIndex=edgeA.nodeIndex();var valueA=nodeA[fieldName]();edgeB.edgeIndex=indexB;nodeB.nodeIndex=edgeB.nodeIndex();var valueB=nodeB[fieldName]();var result=valueA<valueB?-1:(valueA>valueB?1:0);return ascending?result:-result;}
function compareEdgeAndNode(indexA,indexB){var result=compareEdgeFieldName(ascending1,indexA,indexB);if(result===0)
result=compareNodeField(fieldName2,ascending2,indexA,indexB);if(result===0)
return indexA-indexB;return result;}
function compareNodeAndEdge(indexA,indexB){var result=compareNodeField(fieldName1,ascending1,indexA,indexB);if(result===0)
result=compareEdgeFieldName(ascending2,indexA,indexB);if(result===0)
return indexA-indexB;return result;}
function compareNodeAndNode(indexA,indexB){var result=compareNodeField(fieldName1,ascending1,indexA,indexB);if(result===0)
result=compareNodeField(fieldName2,ascending2,indexA,indexB);if(result===0)
return indexA-indexB;return result;}
if(fieldName1==='!edgeName')
this._iterationOrder.sortRange(compareEdgeAndNode,leftBound,rightBound,windowLeft,windowRight);else if(fieldName2==='!edgeName')
this._iterationOrder.sortRange(compareNodeAndEdge,leftBound,rightBound,windowLeft,windowRight);else
this._iterationOrder.sortRange(compareNodeAndNode,leftBound,rightBound,windowLeft,windowRight);}};HeapSnapshotWorker.HeapSnapshotNodesProvider=class extends HeapSnapshotWorker.HeapSnapshotItemProvider{constructor(snapshot,nodeIndexes){var indexProvider=new HeapSnapshotWorker.HeapSnapshotNodeIndexProvider(snapshot);var it=new HeapSnapshotWorker.HeapSnapshotIndexRangeIterator(indexProvider,nodeIndexes);super(it,indexProvider);this.snapshot=snapshot;}
nodePosition(snapshotObjectId){this._createIterationOrder();var node=this.snapshot.createNode();for(var i=0;i<this._iterationOrder.length;i++){node.nodeIndex=this._iterationOrder[i];if(node.id()===snapshotObjectId)
break;}
if(i===this._iterationOrder.length)
return-1;var targetNodeIndex=this._iterationOrder[i];var smallerCount=0;var compare=this._buildCompareFunction(this._currentComparator);for(var i=0;i<this._iterationOrder.length;i++){if(compare(this._iterationOrder[i],targetNodeIndex)<0)
++smallerCount;}
return smallerCount;}
_buildCompareFunction(comparator){var nodeA=this.snapshot.createNode();var nodeB=this.snapshot.createNode();var fieldAccessor1=nodeA[comparator.fieldName1];var fieldAccessor2=nodeA[comparator.fieldName2];var ascending1=comparator.ascending1?1:-1;var ascending2=comparator.ascending2?1:-1;function sortByNodeField(fieldAccessor,ascending){var valueA=fieldAccessor.call(nodeA);var valueB=fieldAccessor.call(nodeB);return valueA<valueB?-ascending:(valueA>valueB?ascending:0);}
function sortByComparator(indexA,indexB){nodeA.nodeIndex=indexA;nodeB.nodeIndex=indexB;var result=sortByNodeField(fieldAccessor1,ascending1);if(result===0)
result=sortByNodeField(fieldAccessor2,ascending2);return result||indexA-indexB;}
return sortByComparator;}
sort(comparator,leftBound,rightBound,windowLeft,windowRight){this._iterationOrder.sortRange(this._buildCompareFunction(comparator),leftBound,rightBound,windowLeft,windowRight);}};HeapSnapshotWorker.JSHeapSnapshot=class extends HeapSnapshotWorker.HeapSnapshot{constructor(profile,progress){super(profile,progress);this._nodeFlags={canBeQueried:1,detachedDOMTreeNode:2,pageObject:4};this._lazyStringCache={};this.initialize();}
createNode(nodeIndex){return new HeapSnapshotWorker.JSHeapSnapshotNode(this,nodeIndex===undefined?-1:nodeIndex);}
createEdge(edgeIndex){return new HeapSnapshotWorker.JSHeapSnapshotEdge(this,edgeIndex);}
createRetainingEdge(retainerIndex){return new HeapSnapshotWorker.JSHeapSnapshotRetainerEdge(this,retainerIndex);}
containmentEdgesFilter(){return edge=>!edge.isInvisible();}
retainingEdgesFilter(){var containmentEdgesFilter=this.containmentEdgesFilter();function filter(edge){return containmentEdgesFilter(edge)&&!edge.node().isRoot()&&!edge.isWeak();}
return filter;}
calculateFlags(){this._flags=new Uint32Array(this.nodeCount);this._markDetachedDOMTreeNodes();this._markQueriableHeapObjects();this._markPageOwnedNodes();}
calculateDistances(){function filter(node,edge){if(node.isHidden())
return edge.name()!=='sloppy_function_map'||node.rawName()!=='system / NativeContext';if(node.isArray()){if(node.rawName()!=='(map descriptors)')
return true;var index=edge.name();return index<2||(index%3)!==1;}
return true;}
super.calculateDistances(filter);}
isUserRoot(node){return node.isUserRoot()||node.isDocumentDOMTreesRoot();}
forEachRoot(action,userRootsOnly){function getChildNodeByName(node,name){for(var iter=node.edges();iter.hasNext();iter.next()){var child=iter.edge.node();if(child.name()===name)
return child;}
return null;}
var visitedNodes={};function doAction(node){var ordinal=node.ordinal();if(!visitedNodes[ordinal]){action(node);visitedNodes[ordinal]=true;}}
var gcRoots=getChildNodeByName(this.rootNode(),'(GC roots)');if(!gcRoots)
return;if(userRootsOnly){for(var iter=this.rootNode().edges();iter.hasNext();iter.next()){var node=iter.edge.node();if(this.isUserRoot(node))
doAction(node);}}else{for(var iter=gcRoots.edges();iter.hasNext();iter.next()){var subRoot=iter.edge.node();for(var iter2=subRoot.edges();iter2.hasNext();iter2.next())
doAction(iter2.edge.node());doAction(subRoot);}
for(var iter=this.rootNode().edges();iter.hasNext();iter.next())
doAction(iter.edge.node());}}
userObjectsMapAndFlag(){return{map:this._flags,flag:this._nodeFlags.pageObject};}
_flagsOfNode(node){return this._flags[node.nodeIndex/this._nodeFieldCount];}
_markDetachedDOMTreeNodes(){var flag=this._nodeFlags.detachedDOMTreeNode;var detachedDOMTreesRoot;for(var iter=this.rootNode().edges();iter.hasNext();iter.next()){var node=iter.edge.node();if(node.name()==='(Detached DOM trees)'){detachedDOMTreesRoot=node;break;}}
if(!detachedDOMTreesRoot)
return;var detachedDOMTreeRE=/^Detached DOM tree/;for(var iter=detachedDOMTreesRoot.edges();iter.hasNext();iter.next()){var node=iter.edge.node();if(detachedDOMTreeRE.test(node.className())){for(var edgesIter=node.edges();edgesIter.hasNext();edgesIter.next())
this._flags[edgesIter.edge.node().nodeIndex/this._nodeFieldCount]|=flag;}}}
_markQueriableHeapObjects(){var flag=this._nodeFlags.canBeQueried;var hiddenEdgeType=this._edgeHiddenType;var internalEdgeType=this._edgeInternalType;var invisibleEdgeType=this._edgeInvisibleType;var weakEdgeType=this._edgeWeakType;var edgeToNodeOffset=this._edgeToNodeOffset;var edgeTypeOffset=this._edgeTypeOffset;var edgeFieldsCount=this._edgeFieldsCount;var containmentEdges=this.containmentEdges;var nodeFieldCount=this._nodeFieldCount;var firstEdgeIndexes=this._firstEdgeIndexes;var flags=this._flags;var list=[];for(var iter=this.rootNode().edges();iter.hasNext();iter.next()){if(iter.edge.node().isUserRoot())
list.push(iter.edge.node().nodeIndex/nodeFieldCount);}
while(list.length){var nodeOrdinal=list.pop();if(flags[nodeOrdinal]&flag)
continue;flags[nodeOrdinal]|=flag;var beginEdgeIndex=firstEdgeIndexes[nodeOrdinal];var endEdgeIndex=firstEdgeIndexes[nodeOrdinal+1];for(var edgeIndex=beginEdgeIndex;edgeIndex<endEdgeIndex;edgeIndex+=edgeFieldsCount){var childNodeIndex=containmentEdges[edgeIndex+edgeToNodeOffset];var childNodeOrdinal=childNodeIndex/nodeFieldCount;if(flags[childNodeOrdinal]&flag)
continue;var type=containmentEdges[edgeIndex+edgeTypeOffset];if(type===hiddenEdgeType||type===invisibleEdgeType||type===internalEdgeType||type===weakEdgeType)
continue;list.push(childNodeOrdinal);}}}
_markPageOwnedNodes(){var edgeShortcutType=this._edgeShortcutType;var edgeElementType=this._edgeElementType;var edgeToNodeOffset=this._edgeToNodeOffset;var edgeTypeOffset=this._edgeTypeOffset;var edgeFieldsCount=this._edgeFieldsCount;var edgeWeakType=this._edgeWeakType;var firstEdgeIndexes=this._firstEdgeIndexes;var containmentEdges=this.containmentEdges;var nodeFieldCount=this._nodeFieldCount;var nodesCount=this.nodeCount;var flags=this._flags;var pageObjectFlag=this._nodeFlags.pageObject;var nodesToVisit=new Uint32Array(nodesCount);var nodesToVisitLength=0;var rootNodeOrdinal=this._rootNodeIndex/nodeFieldCount;var node=this.rootNode();for(var edgeIndex=firstEdgeIndexes[rootNodeOrdinal],endEdgeIndex=firstEdgeIndexes[rootNodeOrdinal+1];edgeIndex<endEdgeIndex;edgeIndex+=edgeFieldsCount){var edgeType=containmentEdges[edgeIndex+edgeTypeOffset];var nodeIndex=containmentEdges[edgeIndex+edgeToNodeOffset];if(edgeType===edgeElementType){node.nodeIndex=nodeIndex;if(!node.isDocumentDOMTreesRoot())
continue;}else if(edgeType!==edgeShortcutType){continue;}
var nodeOrdinal=nodeIndex/nodeFieldCount;nodesToVisit[nodesToVisitLength++]=nodeOrdinal;flags[nodeOrdinal]|=pageObjectFlag;}
while(nodesToVisitLength){var nodeOrdinal=nodesToVisit[--nodesToVisitLength];var beginEdgeIndex=firstEdgeIndexes[nodeOrdinal];var endEdgeIndex=firstEdgeIndexes[nodeOrdinal+1];for(var edgeIndex=beginEdgeIndex;edgeIndex<endEdgeIndex;edgeIndex+=edgeFieldsCount){var childNodeIndex=containmentEdges[edgeIndex+edgeToNodeOffset];var childNodeOrdinal=childNodeIndex/nodeFieldCount;if(flags[childNodeOrdinal]&pageObjectFlag)
continue;var type=containmentEdges[edgeIndex+edgeTypeOffset];if(type===edgeWeakType)
continue;nodesToVisit[nodesToVisitLength++]=childNodeOrdinal;flags[childNodeOrdinal]|=pageObjectFlag;}}}
calculateStatistics(){var nodeFieldCount=this._nodeFieldCount;var nodes=this.nodes;var nodesLength=nodes.length;var nodeTypeOffset=this._nodeTypeOffset;var nodeSizeOffset=this._nodeSelfSizeOffset;var nodeNativeType=this._nodeNativeType;var nodeCodeType=this._nodeCodeType;var nodeConsStringType=this._nodeConsStringType;var nodeSlicedStringType=this._nodeSlicedStringType;var distances=this._nodeDistances;var sizeNative=0;var sizeCode=0;var sizeStrings=0;var sizeJSArrays=0;var sizeSystem=0;var node=this.rootNode();for(var nodeIndex=0;nodeIndex<nodesLength;nodeIndex+=nodeFieldCount){var nodeSize=nodes[nodeIndex+nodeSizeOffset];var ordinal=nodeIndex/nodeFieldCount;if(distances[ordinal]>=HeapSnapshotModel.baseSystemDistance){sizeSystem+=nodeSize;continue;}
var nodeType=nodes[nodeIndex+nodeTypeOffset];node.nodeIndex=nodeIndex;if(nodeType===nodeNativeType)
sizeNative+=nodeSize;else if(nodeType===nodeCodeType)
sizeCode+=nodeSize;else if(nodeType===nodeConsStringType||nodeType===nodeSlicedStringType||node.type()==='string')
sizeStrings+=nodeSize;else if(node.name()==='Array')
sizeJSArrays+=this._calculateArraySize(node);}
this._statistics=new HeapSnapshotModel.Statistics();this._statistics.total=this.totalSize;this._statistics.v8heap=this.totalSize-sizeNative;this._statistics.native=sizeNative;this._statistics.code=sizeCode;this._statistics.jsArrays=sizeJSArrays;this._statistics.strings=sizeStrings;this._statistics.system=sizeSystem;}
_calculateArraySize(node){var size=node.selfSize();var beginEdgeIndex=node.edgeIndexesStart();var endEdgeIndex=node.edgeIndexesEnd();var containmentEdges=this.containmentEdges;var strings=this.strings;var edgeToNodeOffset=this._edgeToNodeOffset;var edgeTypeOffset=this._edgeTypeOffset;var edgeNameOffset=this._edgeNameOffset;var edgeFieldsCount=this._edgeFieldsCount;var edgeInternalType=this._edgeInternalType;for(var edgeIndex=beginEdgeIndex;edgeIndex<endEdgeIndex;edgeIndex+=edgeFieldsCount){var edgeType=containmentEdges[edgeIndex+edgeTypeOffset];if(edgeType!==edgeInternalType)
continue;var edgeName=strings[containmentEdges[edgeIndex+edgeNameOffset]];if(edgeName!=='elements')
continue;var elementsNodeIndex=containmentEdges[edgeIndex+edgeToNodeOffset];node.nodeIndex=elementsNodeIndex;if(node.retainersCount()===1)
size+=node.selfSize();break;}
return size;}
getStatistics(){return this._statistics;}};HeapSnapshotWorker.JSHeapSnapshotNode=class extends HeapSnapshotWorker.HeapSnapshotNode{constructor(snapshot,nodeIndex){super(snapshot,nodeIndex);}
canBeQueried(){var flags=this._snapshot._flagsOfNode(this);return!!(flags&this._snapshot._nodeFlags.canBeQueried);}
rawName(){return super.name();}
name(){var snapshot=this._snapshot;if(this.rawType()===snapshot._nodeConsStringType){var string=snapshot._lazyStringCache[this.nodeIndex];if(typeof string==='undefined'){string=this._consStringName();snapshot._lazyStringCache[this.nodeIndex]=string;}
return string;}
return this.rawName();}
_consStringName(){var snapshot=this._snapshot;var consStringType=snapshot._nodeConsStringType;var edgeInternalType=snapshot._edgeInternalType;var edgeFieldsCount=snapshot._edgeFieldsCount;var edgeToNodeOffset=snapshot._edgeToNodeOffset;var edgeTypeOffset=snapshot._edgeTypeOffset;var edgeNameOffset=snapshot._edgeNameOffset;var strings=snapshot.strings;var edges=snapshot.containmentEdges;var firstEdgeIndexes=snapshot._firstEdgeIndexes;var nodeFieldCount=snapshot._nodeFieldCount;var nodeTypeOffset=snapshot._nodeTypeOffset;var nodeNameOffset=snapshot._nodeNameOffset;var nodes=snapshot.nodes;var nodesStack=[];nodesStack.push(this.nodeIndex);var name='';while(nodesStack.length&&name.length<1024){var nodeIndex=nodesStack.pop();if(nodes[nodeIndex+nodeTypeOffset]!==consStringType){name+=strings[nodes[nodeIndex+nodeNameOffset]];continue;}
var nodeOrdinal=nodeIndex/nodeFieldCount;var beginEdgeIndex=firstEdgeIndexes[nodeOrdinal];var endEdgeIndex=firstEdgeIndexes[nodeOrdinal+1];var firstNodeIndex=0;var secondNodeIndex=0;for(var edgeIndex=beginEdgeIndex;edgeIndex<endEdgeIndex&&(!firstNodeIndex||!secondNodeIndex);edgeIndex+=edgeFieldsCount){var edgeType=edges[edgeIndex+edgeTypeOffset];if(edgeType===edgeInternalType){var edgeName=strings[edges[edgeIndex+edgeNameOffset]];if(edgeName==='first')
firstNodeIndex=edges[edgeIndex+edgeToNodeOffset];else if(edgeName==='second')
secondNodeIndex=edges[edgeIndex+edgeToNodeOffset];}}
nodesStack.push(secondNodeIndex);nodesStack.push(firstNodeIndex);}
return name;}
className(){var type=this.type();switch(type){case'hidden':return'(system)';case'object':case'native':return this.name();case'code':return'(compiled code)';default:return'('+type+')';}}
classIndex(){var snapshot=this._snapshot;var nodes=snapshot.nodes;var type=nodes[this.nodeIndex+snapshot._nodeTypeOffset];if(type===snapshot._nodeObjectType||type===snapshot._nodeNativeType)
return nodes[this.nodeIndex+snapshot._nodeNameOffset];return-1-type;}
id(){var snapshot=this._snapshot;return snapshot.nodes[this.nodeIndex+snapshot._nodeIdOffset];}
isHidden(){return this.rawType()===this._snapshot._nodeHiddenType;}
isArray(){return this.rawType()===this._snapshot._nodeArrayType;}
isSynthetic(){return this.rawType()===this._snapshot._nodeSyntheticType;}
isUserRoot(){return!this.isSynthetic();}
isDocumentDOMTreesRoot(){return this.isSynthetic()&&this.name()==='(Document DOM trees)';}
serialize(){var result=super.serialize();var flags=this._snapshot._flagsOfNode(this);if(flags&this._snapshot._nodeFlags.canBeQueried)
result.canBeQueried=true;if(flags&this._snapshot._nodeFlags.detachedDOMTreeNode)
result.detachedDOMTreeNode=true;return result;}};HeapSnapshotWorker.JSHeapSnapshotEdge=class extends HeapSnapshotWorker.HeapSnapshotEdge{constructor(snapshot,edgeIndex){super(snapshot,edgeIndex);}
clone(){var snapshot=(this._snapshot);return new HeapSnapshotWorker.JSHeapSnapshotEdge(snapshot,this.edgeIndex);}
hasStringName(){if(!this.isShortcut())
return this._hasStringName();return isNaN(parseInt(this._name(),10));}
isElement(){return this.rawType()===this._snapshot._edgeElementType;}
isHidden(){return this.rawType()===this._snapshot._edgeHiddenType;}
isWeak(){return this.rawType()===this._snapshot._edgeWeakType;}
isInternal(){return this.rawType()===this._snapshot._edgeInternalType;}
isInvisible(){return this.rawType()===this._snapshot._edgeInvisibleType;}
isShortcut(){return this.rawType()===this._snapshot._edgeShortcutType;}
name(){var name=this._name();if(!this.isShortcut())
return String(name);var numName=parseInt(name,10);return String(isNaN(numName)?name:numName);}
toString(){var name=this.name();switch(this.type()){case'context':return'->'+name;case'element':return'['+name+']';case'weak':return'[['+name+']]';case'property':return name.indexOf(' ')===-1?'.'+name:'["'+name+'"]';case'shortcut':if(typeof name==='string')
return name.indexOf(' ')===-1?'.'+name:'["'+name+'"]';else
return'['+name+']';case'internal':case'hidden':case'invisible':return'{'+name+'}';}
return'?'+name+'?';}
_hasStringName(){var type=this.rawType();var snapshot=this._snapshot;return type!==snapshot._edgeElementType&&type!==snapshot._edgeHiddenType;}
_name(){return this._hasStringName()?this._snapshot.strings[this._nameOrIndex()]:this._nameOrIndex();}
_nameOrIndex(){return this._edges[this.edgeIndex+this._snapshot._edgeNameOffset];}
rawType(){return this._edges[this.edgeIndex+this._snapshot._edgeTypeOffset];}};HeapSnapshotWorker.JSHeapSnapshotRetainerEdge=class extends HeapSnapshotWorker.HeapSnapshotRetainerEdge{constructor(snapshot,retainerIndex){super(snapshot,retainerIndex);}
clone(){var snapshot=(this._snapshot);return new HeapSnapshotWorker.JSHeapSnapshotRetainerEdge(snapshot,this.retainerIndex());}
isHidden(){return this._edge().isHidden();}
isInternal(){return this._edge().isInternal();}
isInvisible(){return this._edge().isInvisible();}
isShortcut(){return this._edge().isShortcut();}
isWeak(){return this._edge().isWeak();}};(function disableLoggingForTest(){if(self.Runtime&&Runtime.queryParam('test'))
console.warn=()=>undefined;})();;HeapSnapshotWorker.HeapSnapshotLoader=class{constructor(dispatcher){this._reset();this._progress=new HeapSnapshotWorker.HeapSnapshotProgress(dispatcher);}
dispose(){this._reset();}
_reset(){this._json='';this._state='find-snapshot-info';this._snapshot={};}
close(){if(this._json)
this._parseStringsArray();}
buildSnapshot(){this._progress.updateStatus('Processing snapshot\u2026');var result=new HeapSnapshotWorker.JSHeapSnapshot(this._snapshot,this._progress);this._reset();return result;}
_parseUintArray(){var index=0;var char0='0'.charCodeAt(0),char9='9'.charCodeAt(0),closingBracket=']'.charCodeAt(0);var length=this._json.length;while(true){while(index<length){var code=this._json.charCodeAt(index);if(char0<=code&&code<=char9){break;}else if(code===closingBracket){this._json=this._json.slice(index+1);return false;}
++index;}
if(index===length){this._json='';return true;}
var nextNumber=0;var startIndex=index;while(index<length){var code=this._json.charCodeAt(index);if(char0>code||code>char9)
break;nextNumber*=10;nextNumber+=(code-char0);++index;}
if(index===length){this._json=this._json.slice(startIndex);return true;}
this._array[this._arrayIndex++]=nextNumber;}}
_parseStringsArray(){this._progress.updateStatus('Parsing strings\u2026');var closingBracketIndex=this._json.lastIndexOf(']');if(closingBracketIndex===-1)
throw new Error('Incomplete JSON');this._json=this._json.slice(0,closingBracketIndex+1);this._snapshot.strings=JSON.parse(this._json);}
write(chunk){if(this._json!==null)
this._json+=chunk;while(true){switch(this._state){case'find-snapshot-info':{var snapshotToken='"snapshot"';var snapshotTokenIndex=this._json.indexOf(snapshotToken);if(snapshotTokenIndex===-1)
throw new Error('Snapshot token not found');var json=this._json.slice(snapshotTokenIndex+snapshotToken.length+1);this._state='parse-snapshot-info';this._progress.updateStatus('Loading snapshot info\u2026');this._json=null;this._jsonTokenizer=new TextUtils.TextUtils.BalancedJSONTokenizer(this._writeBalancedJSON.bind(this));chunk=json;}
case'parse-snapshot-info':{this._jsonTokenizer.write(chunk);if(this._jsonTokenizer)
return;break;}
case'find-nodes':{var nodesToken='"nodes"';var nodesTokenIndex=this._json.indexOf(nodesToken);if(nodesTokenIndex===-1)
return;var bracketIndex=this._json.indexOf('[',nodesTokenIndex);if(bracketIndex===-1)
return;this._json=this._json.slice(bracketIndex+1);var node_fields_count=this._snapshot.snapshot.meta.node_fields.length;var nodes_length=this._snapshot.snapshot.node_count*node_fields_count;this._array=new Uint32Array(nodes_length);this._arrayIndex=0;this._state='parse-nodes';break;}
case'parse-nodes':{var hasMoreData=this._parseUintArray();this._progress.updateProgress('Loading nodes\u2026 %d%%',this._arrayIndex,this._array.length);if(hasMoreData)
return;this._snapshot.nodes=this._array;this._state='find-edges';this._array=null;break;}
case'find-edges':{var edgesToken='"edges"';var edgesTokenIndex=this._json.indexOf(edgesToken);if(edgesTokenIndex===-1)
return;var bracketIndex=this._json.indexOf('[',edgesTokenIndex);if(bracketIndex===-1)
return;this._json=this._json.slice(bracketIndex+1);var edge_fields_count=this._snapshot.snapshot.meta.edge_fields.length;var edges_length=this._snapshot.snapshot.edge_count*edge_fields_count;this._array=new Uint32Array(edges_length);this._arrayIndex=0;this._state='parse-edges';break;}
case'parse-edges':{var hasMoreData=this._parseUintArray();this._progress.updateProgress('Loading edges\u2026 %d%%',this._arrayIndex,this._array.length);if(hasMoreData)
return;this._snapshot.edges=this._array;this._array=null;if(this._snapshot.snapshot.trace_function_count){this._state='find-trace-function-infos';this._progress.updateStatus('Loading allocation traces\u2026');}else if(this._snapshot.snapshot.meta.sample_fields){this._state='find-samples';this._progress.updateStatus('Loading samples\u2026');}else{this._state='find-strings';}
break;}
case'find-trace-function-infos':{var tracesToken='"trace_function_infos"';var tracesTokenIndex=this._json.indexOf(tracesToken);if(tracesTokenIndex===-1)
return;var bracketIndex=this._json.indexOf('[',tracesTokenIndex);if(bracketIndex===-1)
return;this._json=this._json.slice(bracketIndex+1);var trace_function_info_field_count=this._snapshot.snapshot.meta.trace_function_info_fields.length;var trace_function_info_length=this._snapshot.snapshot.trace_function_count*trace_function_info_field_count;this._array=new Uint32Array(trace_function_info_length);this._arrayIndex=0;this._state='parse-trace-function-infos';break;}
case'parse-trace-function-infos':{if(this._parseUintArray())
return;this._snapshot.trace_function_infos=this._array;this._array=null;this._state='find-trace-tree';break;}
case'find-trace-tree':{var tracesToken='"trace_tree"';var tracesTokenIndex=this._json.indexOf(tracesToken);if(tracesTokenIndex===-1)
return;var bracketIndex=this._json.indexOf('[',tracesTokenIndex);if(bracketIndex===-1)
return;this._json=this._json.slice(bracketIndex);this._state='parse-trace-tree';break;}
case'parse-trace-tree':{var nextToken=this._snapshot.snapshot.meta.sample_fields?'"samples"':'"strings"';var nextTokenIndex=this._json.indexOf(nextToken);if(nextTokenIndex===-1)
return;var bracketIndex=this._json.lastIndexOf(']',nextTokenIndex);this._snapshot.trace_tree=JSON.parse(this._json.substring(0,bracketIndex+1));this._json=this._json.slice(bracketIndex+1);if(this._snapshot.snapshot.meta.sample_fields){this._state='find-samples';this._progress.updateStatus('Loading samples\u2026');}else{this._state='find-strings';this._progress.updateStatus('Loading strings\u2026');}
break;}
case'find-samples':{var samplesToken='"samples"';var samplesTokenIndex=this._json.indexOf(samplesToken);if(samplesTokenIndex===-1)
return;var bracketIndex=this._json.indexOf('[',samplesTokenIndex);if(bracketIndex===-1)
return;this._json=this._json.slice(bracketIndex+1);this._array=[];this._arrayIndex=0;this._state='parse-samples';break;}
case'parse-samples':{if(this._parseUintArray())
return;this._snapshot.samples=this._array;this._array=null;this._state='find-strings';this._progress.updateStatus('Loading strings\u2026');break;}
case'find-strings':{var stringsToken='"strings"';var stringsTokenIndex=this._json.indexOf(stringsToken);if(stringsTokenIndex===-1)
return;var bracketIndex=this._json.indexOf('[',stringsTokenIndex);if(bracketIndex===-1)
return;this._json=this._json.slice(bracketIndex);this._state='accumulate-strings';break;}
case'accumulate-strings':return;}}}
_writeBalancedJSON(data){this._json=this._jsonTokenizer.remainder();this._jsonTokenizer=null;this._state='find-nodes';this._snapshot.snapshot=(JSON.parse(data));}};;HeapSnapshotWorker.HeapSnapshotWorkerDispatcher=class{constructor(globalObject,postMessage){this._objects=[];this._global=globalObject;this._postMessage=postMessage;}
_findFunction(name){var path=name.split('.');var result=this._global;for(var i=0;i<path.length;++i)
result=result[path[i]];return result;}
sendEvent(name,data){this._postMessage({eventName:name,data:data});}
dispatchMessage(event){var data=(event.data);var response={callId:data.callId};try{switch(data.disposition){case'create':var constructorFunction=this._findFunction(data.methodName);this._objects[data.objectId]=new constructorFunction(this);break;case'dispose':delete this._objects[data.objectId];break;case'getter':var object=this._objects[data.objectId];var result=object[data.methodName];response.result=result;break;case'factory':var object=this._objects[data.objectId];var result=object[data.methodName].apply(object,data.methodArguments);if(result)
this._objects[data.newObjectId]=result;response.result=!!result;break;case'method':var object=this._objects[data.objectId];response.result=object[data.methodName].apply(object,data.methodArguments);break;case'evaluateForTest':try{response.result=self.eval(data.source);}catch(e){response.result=e.toString();}
break;}}catch(e){response.error=e.toString();response.errorCallStack=e.stack;if(data.methodName)
response.errorMethodName=data.methodName;}
this._postMessage(response);}};;function postMessageWrapper(message){postMessage(message);}
var dispatcher=new HeapSnapshotWorker.HeapSnapshotWorkerDispatcher(this,postMessageWrapper);function installMessageEventListener(listener){self.addEventListener('message',listener,false);}
installMessageEventListener(dispatcher.dispatchMessage.bind(dispatcher));;