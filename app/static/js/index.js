var decisionVue = new Vue({
		el: '#app',
		data: function () {
			return {
			    dialogBooleanTableVisible:false,
			    dialogTableVisible:false,
				trueSwitch:true,
				falseSwitch:false,
                activeIndex:0,
				netItemType:1,
                c1Index:1,
                edgeId:1,
                net:'',
                netData : {
                    nodes: [
                        {
                            id:1,
                            shape:'circle',
                            label:'起始',
                            x:500,
                            y:50
                        }
                    ],
                    edges: []
                },
                form:{
                    type:2,
                    conditions:[
                        {
                        	option:'条件选项1',
                            typeOption:'<',
                            condition:1.0,
                            content:'新节点'
                        }
                    ],
                    booleanValues: {
                    	booleanOption:'选项1',
						trueContent: 'true节点',
						falseContent: 'false节点',

					}
                },
				line:{
			    	hasCondition:'有',
					condition:''
				},
                booleanOptions:[
                    {value:'选项1',label:'选项1'},
                    {value:'选项2',label:'选项2'}
                ],
                conditionOptions:[
                	{value:'条件选项1',label:'条件选项1'},
                    {value:'条件选项2',label:'条件选项2'}
                ],
                conditionTypeOptions:[
                	{value:'<',label:'小于'},
                    {value:'≤',label:'小于等于'},
					{value:'＝',label:'等于'},
					{value:'≥',label:'大于等于'},
					{value:'>',label:'大于'},
				]
            }
		},
        methods: {
		    handleConditionDel:function(index,row){
		        this.conditionOptions.splice(index, 1);
            },
            addRow:function(){
		        var index = this.conditionOptions.length;
		        this.conditionOptions.push(
		            {value:'条件选项'+(index+1),label:'条件选项'+(index+1)},
                    );
            },
		    handleBooleanDel:function(index,row){
		        this.booleanOptions.splice(index, 1);
            },
            addBooleanRow:function(){
		        var index = this.booleanOptions.length;
		        this.booleanOptions.push(
		            {value:'选项'+(index+1),label:'选项'+(index+1)},
                    );
            },
            changeBoolean:function () {

			},
			changeCondition:function(){

            },
            changeConditionType:function(){

            },
            // 添加一个条件
            addCondition:function(conditionIndex){
            	var defaultCondition = {
                        	option:'条件选项1',
                            typeOption:'<',
                            condition:2.0,
                            content:'新节点'
                        };
                decisionVue.form.conditions.splice(conditionIndex+1, 0, defaultCondition);
            },
            // 删除一个条件
            delCondition:function(conditionIndex){
            	if(conditionIndex==0){
                    this.$notify({
                          title: '提示',
                          message: '仅有一个条件，不能删除',
                        });
                    return false;
                }else{
                    decisionVue.form.conditions.splice(conditionIndex, 1);
                }
            },
            // 添加是非判断
            addBooleanNode:function(){
            	var beforeIndex = this.c1Index;
            	var booleanValues = this.form.booleanValues;

            	this.c1Index++;
                this.edgeId++;
            	// 添加boolean option
                var sourceX = this.net.find(this.activeIndex).getCenter().x;
            	var targetY = this.net.find(this.activeIndex).getCenter().y+100;

            	this.net.add('node', {
                    shape: 'rhombus',
                    id: this.c1Index,
                    label:booleanValues.booleanOption,
                    x: sourceX,
                    y: targetY
                });
                this.net.add('edge',{
                    source: this.activeIndex,
                    target: this.c1Index,
                    label: '',
                    id: 'edgeId'+this.edgeId,
                    sourceAnchor:4,
                    targetAnchor:2,
                });

                //添加两个结果
                beforeIndex = this.c1Index;
                var childrenX = this.getXValue(sourceX, 2);
                targetY = targetY+80;
                this.c1Index++;
                this.edgeId++;
                this.net.add('node', {
                    shape: 'rect',
                    id: this.c1Index,
                    label:booleanValues.trueContent,
                    x: childrenX[0],
                    y: targetY
                });
                this.net.add('edge',{
                    source: beforeIndex,
                    target: this.c1Index,
                    label: '是',
                    id: 'edgeId'+this.edgeId,
                    sourceAnchor:4,
                    targetAnchor:2,
                });
                this.c1Index++;
                this.edgeId++;
                this.net.add('node', {
                    shape: 'rect',
                    id: this.c1Index,
                    label:booleanValues.falseContent,
                    x: childrenX[1],
                    y: targetY
                });
                this.net.add('edge',{
                    source: beforeIndex,
                    target: this.c1Index,
                    label: '否',
                    id: 'edgeId'+this.edgeId,
                    sourceAnchor:4,
                    targetAnchor:2,
                });
                this.net.refresh();
            },

            //添加多个条件判断
            addConditionNode:function(){
            	var conditions = this.form.conditions;
            	var sourceX = this.net.find(this.activeIndex).getCenter().x;
            	var childrenX = this.getXValue(sourceX,conditions.length);
            	var targetY = this.net.find(this.activeIndex).getCenter().y+80;
            	for(var i=0;i<conditions.length;i++){
            		var condition = conditions[i];
                    this.c1Index++;
                    this.edgeId++;
                    this.net.add('node', {
                        shape: 'rect',
                        id: this.c1Index,
                        label:condition.content,
                        x: childrenX[i],
                        y: targetY
                    });
                    this.net.add('edge',{
                        source: this.activeIndex,
                        target: this.c1Index,
                        label: condition.option+condition.typeOption+condition.condition,
                        id: 'edgeId'+this.edgeId,
						sourceAnchor:4,
						targetAnchor:2,
                    });

                }
                this.net.refresh();
            },
			addEdge:function(){
		    	this.edgeId++;
		    	if(this.line.hasCondition=='有'){
		    		this.net.beginAdd('edge', {
						shape: 'VHV',
						arrow:true,
						id: 'edgeId'+this.edgeId,
						source: this.activeIndex,
						label:this.line.condition
					});
				}else{
		    		this.net.beginAdd('edge', {
						shape: 'VHV',
						arrow:true,
						id: 'edgeId'+this.edgeId,
						source: this.activeIndex
					});
				}
			},
			updo:function(){
		    	this.net.updo();
			},
            initNet:function(){
            	var _this = this;
                // 下面覆盖默认的锚点位置
                G6.registNode('rect', {
                    getAnchorPoints: function(){
                      return [
                        [0, 0.5],   // 左边中点
                        [1, 0.5],   // 右边中点
                        [0.5, 0],   // 上边中点
                        [0.5, 1]    // 下边中点
                      ];
                    }
                  });
                G6.registNode('circle', {
                    getAnchorPoints: function(){
                      return [
                        [0, 0.5],   // 左边中点
                        [1, 0.5],   // 右边中点
                        [0.5, 0],   // 上边中点
                        [0.5, 1]    // 下边中点
                      ];
                    }
                  });
                G6.registNode('rhombus', {
                    getAnchorPoints: function(){
                      return [
                        [0, 0.5],   // 左边中点
                        [1, 0.5],   // 右边中点
                        [0.5, 0],   // 上边中点
                        [0.5, 1]    // 下边中点
                      ];
                    }
                  });

                _this.net = new G6.Net({
                    id: 'c1',           // 容器ID
                    height: 500,        // 画布高
					rollback: true,     // 是否启用回滚机制
                });
                _this.net.source(_this.netData.nodes, _this.netData.edges);
                _this.net.edge().shape('VHV').style({
                    arrow: true
                  });
                _this.net.render();
                _this.net.on('itemactived', function(ev){
                    if(G6.Util.isNode(ev.item)){
                        _this.activeIndex = ev.item.getModel().id;
						_this.netItemType = 1;
					}else if(G6.Util.isEdge(ev.item)){
						_this.netItemType = 2;
					}else{
						_this.netItemType = 0;
					}
                });
                _this.net.on('itemunactived', function(ev){
                    if(G6.Util.isNode(ev.item)){
						_this.netItemType = 1;
                        _this.activeIndex = 0;
                    }else if(G6.Util.isEdge(ev.item)){
						_this.netItemType = 2;
						_this.activeIndex = 0;
					}else{
						_this.netItemType = 0;
                    	_this.activeIndex = 0;
					}
                });

            },
            getXValue:function (sourceX, childNumber) {
                var xValues = [];
                if(childNumber%2==0){
                    var halfNumber = childNumber/2;
                    for(var i=0;i<childNumber;i++){
                        if(i<halfNumber){
                            xValues.push(sourceX-150*(halfNumber-i)+75);
                        }else{
                            xValues.push(sourceX+150*(i-halfNumber)+75);
                        }
                    }
                }else{
                    var halfNumber = (childNumber+1)/2;
                    for(var i=0;i<childNumber;i++){
                        if(i<halfNumber){
                            xValues.push(sourceX-150*(halfNumber-i-1));
                        }else{
                            xValues.push(sourceX+150*(i-halfNumber+1));
                        }
                    }
                }
                return xValues;
			},
            downloadImage:function(bool) {
            	var _this = this;
                var matrixStash = _this.net.getMatrix(); // 缓存当前矩阵
                if (bool) {
                	_this.net.autoZoom(); // 图自动缩放以适应画布尺寸
                }
                html2canvas(_this.net.get('graphContainer'), {
                    onrendered: function(canvas) {
                        var dataURL = canvas.toDataURL('image/png');
                        var link = document.createElement('a');
                        var saveName = 'graph.png';
                        link.download = saveName;
                        link.href = dataURL.replace('image/png', 'image/octet-stream');
                        link.click();
                        _this.net.updateMatrix(matrixStash); // 还原矩阵
                        _this.net.refresh();
                    }
                });
            }
		},

        created: function() {
			// 监听删除键
            var _this = this;
            document.onkeydown = function(e) {
                let key = window.event.keyCode;

                if ((/macintosh|mac os x/i.test(navigator.userAgent)&&key == 8)
					||(/windows|win32/i.test(navigator.userAgent)&&key==46)) {
                    if(_this.netItemType==1){
                    	if(this.activeIndex==1){
                            _this.$notify({
                              title: '提示',
                              message: '根节点不能删除',
                            });
                        }else{
                        	_this.net.remove(_this.net.find(_this.activeIndex));
                        }
                    }
                }
            };
        },
	});
$(function () {
   decisionVue.initNet();
});