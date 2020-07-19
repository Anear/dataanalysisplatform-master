// 是否打开菜单
isCollapse = false;
if(localStorage.hasOwnProperty('isCollapse')){
	isCollapse = JSON.parse(localStorage.isCollapse=='undefined'?'false':localStorage.isCollapse);
}
sideBarMenus = JSON.parse(localStorage.getItem("sideBarMenus"));
if(!sideBarMenus){
	sideBarMenus = [];
}
icons = ['el-icon-star-on','el-icon-printer', 'el-icon-setting','el-icon-share','el-icon-edit','el-icon-location','el-icon-location-outline','el-icon-menu', 'el-icon-tickets'];
// 设置公共方法
Vue.prototype.cuttleAside=function(_isCollapse){
	vm.isCollapse = _isCollapse;
	localStorage.setItem("isCollapse", _isCollapse);
};
Vue.prototype.initLocalUserMenus=function($this){
	// 更新defaultActive
	let pathname = window.location.pathname;
	for(let menu of sideBarMenus){
		if(pathname==menu['url']){
			$this.defaultActive = menu['_id'];
			$this.breadcrumbs = [menu['name']];
		}
		for(let subMenu of menu.children){
			if(pathname == subMenu['url']){
				$this.defaultActive = menu['_id']+'-'+subMenu['_id'];
				$this.breadcrumbs = [menu['name'], subMenu['name']];

			}
		}
	}
};

Vue.prototype.initUserMenus=function($this){
	$.ajax({
			url:'/user/menus/',
			data:{},
			method:'post',
			success:function (data) {
				if(data.status==1&&JSON.stringify(data.data)!=JSON.stringify($this.sideBarMenus)){
					$this.sideBarMenus = data.data;
					localStorage.setItem("sideBarMenus", JSON.stringify(data.data));
					// 更新defaultActive
					let pathname = window.location.pathname;
					for(let menu of data.data){
						if(pathname==menu['url']){
							$this.defaultActive = menu['_id'];
							$this.breadcrumbs = [menu['name']];
						}
						for(let subMenu of menu.children){
							if(pathname == subMenu['url']){
								$this.defaultActive = menu['_id']+'-'+subMenu['_id'];
								$this.breadcrumbs = [menu['name'], subMenu['name']];
							}
						}
					}
				}else {
					handleError(data, $this);
				}
			},
			error:function (jqXHR, textStatus, errorThrown) {
				$this.$message.error('服务器有异常，请稍后重试');
			}
		});
};
Vue.prototype.initAllMenus=function($this){
	$.ajax({
			url:'/menus/',
			data:{},
			method:'post',
			success:function (data) {
				if(data.status==1){
					$this.allMenus = data.data;
				}else{
					handleError(data, $this);
				}
			},
			error:function (jqXHR, textStatus, errorThrown) {
				$this.$message.error('服务器有异常，请稍后重试');
			}
		});
};
Vue.prototype.initAllResources=function($this){
	$.ajax({
			url:'/resources/',
			data:{},
			method:'post',
			success:function (data) {
				if(data.status==1){
					$this.allResources = data.data;
				}else{
					handleError(data, $this);
				}
			},
			error:function (jqXHR, textStatus, errorThrown) {
				$this.$message.error('服务器有异常，请稍后重试');
			}
		});
};
Vue.prototype.initAllRoles=function($this){
	$.ajax({
			url:'/roles/',
			data:{},
			method:'post',
			success:function (data) {
				if(data.status==1){
					$this.allRoles = data.data;
				}else{
					handleError(data, $this);
				}
			},
			error:function (jqXHR, textStatus, errorThrown) {
				$this.$message.error('服务器有异常，请稍后重试');
			}
		});
};
function getRequest() {
	let url = location.search; //获取url中"?"符后的字串
	let theRequest = {};

	if (url.indexOf("?") !== -1) {
		let str = url.substr(1);
		strs = str.split("&");
		for(let i = 0; i < strs.length; i ++) {
			theRequest[strs[i].split("=")[0]] = unescape(strs[i].split("=")[1]);
		}
	 }
	 return theRequest;
}
function handleError(data, vm){
	let errCode = data['err_code'];
	if(errCode){
		let href = '';

		switch (errCode) {
			case 401:
				vm.$alert('session超时，请重新登录', '错误提示', {
					showClose:false,
					confirmButtonText: '确定',
					callback: action => {
						window.location.href = '/login/?next='+data['next'];
					}
				});
				break;
			case 403:
				vm.$alert(data['msg'], '错误提示', {
					showClose:false,
					confirmButtonText: '确定',
					callback: action => {

					}
				});
				break;
			case 404:
				vm.$alert(data['msg'], '错误提示', {
					showClose:false,
					confirmButtonText: '确定',
					callback: action => {

					}
				});

				break;
			default:
				vm.$message.error('服务器异常请稍后重试');
		}
	}else if(data['status']==0){
		if(data['msg']){
			vm.$message.error(data['msg']);
		}else{
			vm.$message.error('服务器异常请稍后重试');
		}
	}
}