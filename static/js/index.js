function on_toggle_btn_clicked() {
    const display_type = document.getElementById("navs").style.display;
    // console.log(display_type);
    if (!display_type || display_type === "none") {
        document.getElementById("navs").style.display = "flex";
        document.getElementById("toggle-btn").innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" viewBox=\"0 0 24 24\" width=\"24\" height=\"24\" preserveAspectRatio=\"xMidYMid meet\" style=\"width: 100%; height: 100%; transform: translate3d(0px, 0px, 0px); content-visibility: visible;\"><defs><clipPath id=\"__lottie_element_2\"><rect width=\"24\" height=\"24\" x=\"0\" y=\"0\"></rect></clipPath><clipPath id=\"__lottie_element_16\"><path d=\"M0,0 L24,0 L24,24 L0,24z\"></path></clipPath></defs><g clip-path=\"url(#__lottie_element_2)\"><g clip-path=\"url(#__lottie_element_16)\" transform=\"matrix(1,0,0,1,0,0)\" opacity=\"1\" style=\"display: block;\"><g transform=\"matrix(0.7091159820556641,-0.7050918340682983,0.7050918340682983,0.7091159820556641,14.811344146728516,14.814605712890625)\" opacity=\"1\" style=\"display: block;\"><g opacity=\"1\" transform=\"matrix(1.3328100442886353,0,0,0.9994699954986572,0,0)\"><path fill=\"rgb(0,0,0)\" fill-opacity=\"1\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path><path stroke-linecap=\"butt\" stroke-linejoin=\"miter\" fill-opacity=\"0\" stroke-miterlimit=\"4\" stroke=\"rgb(0,0,0)\" stroke-opacity=\"1\" stroke-width=\"2\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path></g></g><g transform=\"matrix(0,0,0,1,11.968999862670898,16)\" opacity=\"1\" style=\"display: block;\"><g opacity=\"1\" transform=\"matrix(1.3328100442886353,0,0,0.9994699954986572,0,0)\"><path fill=\"rgb(0,0,0)\" fill-opacity=\"1\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path><path stroke-linecap=\"butt\" stroke-linejoin=\"miter\" fill-opacity=\"0\" stroke-miterlimit=\"4\" stroke=\"rgb(0,0,0)\" stroke-opacity=\"1\" stroke-width=\"2\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path></g></g><g transform=\"matrix(0.7091159820556641,0.7050918340682983,-0.7050918340682983,0.7091159820556641,9.181036949157715,14.83504581451416)\" opacity=\"1\" style=\"display: block;\"><g opacity=\"1\" transform=\"matrix(1.3328100442886353,0,0,0.9994699954986572,0,0)\"><path fill=\"rgb(0,0,0)\" fill-opacity=\"1\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path><path stroke-linecap=\"butt\" stroke-linejoin=\"miter\" fill-opacity=\"0\" stroke-miterlimit=\"4\" stroke=\"rgb(0,0,0)\" stroke-opacity=\"1\" stroke-width=\"2\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path></g></g></g></g></svg>";
    }
    else {
        document.getElementById("navs").style.display = "none";
        document.getElementById("toggle-btn").innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" viewBox=\"0 0 24 24\" width=\"32\" height=\"32\" preserveAspectRatio=\"xMidYMid meet\" style=\"width: 100%; height: 100%; transform: translate3d(0px, 0px, 0px); content-visibility: visible;\"><defs><clipPath id=\"__lottie_element_2\"><rect width=\"24\" height=\"24\" x=\"0\" y=\"0\"></rect></clipPath><clipPath id=\"__lottie_element_16\"><path d=\"M0,0 L24,0 L24,24 L0,24z\"></path></clipPath></defs><g clip-path=\"url(#__lottie_element_2)\"><g clip-path=\"url(#__lottie_element_16)\" transform=\"matrix(1,0,0,1,0,0)\" opacity=\"1\" style=\"display: block;\"><g transform=\"matrix(1,0,0,1,12,22)\" opacity=\"1\" style=\"display: block;\"><g opacity=\"1\" transform=\"matrix(1.3328100442886353,0,0,0.9994699954986572,0,0)\"><path fill=\"rgb(0,0,0)\" fill-opacity=\"1\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path><path stroke-linecap=\"butt\" stroke-linejoin=\"miter\" fill-opacity=\"0\" stroke-miterlimit=\"4\" stroke=\"rgb(0,0,0)\" stroke-opacity=\"1\" stroke-width=\"2\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path></g></g><g transform=\"matrix(1,0,0,1,12,16)\" opacity=\"1\" style=\"display: block;\"><g opacity=\"1\" transform=\"matrix(1.3328100442886353,0,0,0.9994699954986572,0,0)\"><path fill=\"rgb(0,0,0)\" fill-opacity=\"1\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path><path stroke-linecap=\"butt\" stroke-linejoin=\"miter\" fill-opacity=\"0\" stroke-miterlimit=\"4\" stroke=\"rgb(0,0,0)\" stroke-opacity=\"1\" stroke-width=\"2\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path></g></g><g transform=\"matrix(1,0,0,1,12,9.998000144958496)\" opacity=\"1\" style=\"display: block;\"><g opacity=\"1\" transform=\"matrix(1.3328100442886353,0,0,0.9994699954986572,0,0)\"><path fill=\"rgb(0,0,0)\" fill-opacity=\"1\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path><path stroke-linecap=\"butt\" stroke-linejoin=\"miter\" fill-opacity=\"0\" stroke-miterlimit=\"4\" stroke=\"rgb(0,0,0)\" stroke-opacity=\"1\" stroke-width=\"2\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path></g></g></g></g></svg>";
    }
}

function on_navs_btn_clicked(id){
    const isMobile = window.matchMedia("(max-width: 1000px)").matches;
    // console.log(isMobile);
    if (isMobile) {
        document.getElementById('navs').style.display = 'none';
        document.getElementById("toggle-btn").innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" viewBox=\"0 0 24 24\" width=\"32\" height=\"32\" preserveAspectRatio=\"xMidYMid meet\" style=\"width: 100%; height: 100%; transform: translate3d(0px, 0px, 0px); content-visibility: visible;\"><defs><clipPath id=\"__lottie_element_2\"><rect width=\"24\" height=\"24\" x=\"0\" y=\"0\"></rect></clipPath><clipPath id=\"__lottie_element_16\"><path d=\"M0,0 L24,0 L24,24 L0,24z\"></path></clipPath></defs><g clip-path=\"url(#__lottie_element_2)\"><g clip-path=\"url(#__lottie_element_16)\" transform=\"matrix(1,0,0,1,0,0)\" opacity=\"1\" style=\"display: block;\"><g transform=\"matrix(1,0,0,1,12,22)\" opacity=\"1\" style=\"display: block;\"><g opacity=\"1\" transform=\"matrix(1.3328100442886353,0,0,0.9994699954986572,0,0)\"><path fill=\"rgb(0,0,0)\" fill-opacity=\"1\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path><path stroke-linecap=\"butt\" stroke-linejoin=\"miter\" fill-opacity=\"0\" stroke-miterlimit=\"4\" stroke=\"rgb(0,0,0)\" stroke-opacity=\"1\" stroke-width=\"2\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path></g></g><g transform=\"matrix(1,0,0,1,12,16)\" opacity=\"1\" style=\"display: block;\"><g opacity=\"1\" transform=\"matrix(1.3328100442886353,0,0,0.9994699954986572,0,0)\"><path fill=\"rgb(0,0,0)\" fill-opacity=\"1\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path><path stroke-linecap=\"butt\" stroke-linejoin=\"miter\" fill-opacity=\"0\" stroke-miterlimit=\"4\" stroke=\"rgb(0,0,0)\" stroke-opacity=\"1\" stroke-width=\"2\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path></g></g><g transform=\"matrix(1,0,0,1,12,9.998000144958496)\" opacity=\"1\" style=\"display: block;\"><g opacity=\"1\" transform=\"matrix(1.3328100442886353,0,0,0.9994699954986572,0,0)\"><path fill=\"rgb(0,0,0)\" fill-opacity=\"1\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path><path stroke-linecap=\"butt\" stroke-linejoin=\"miter\" fill-opacity=\"0\" stroke-miterlimit=\"4\" stroke=\"rgb(0,0,0)\" stroke-opacity=\"1\" stroke-width=\"2\" d=\" M-6,-4 C-6,-4 6,-4 6,-4\"></path></g></g></g></g></svg>";
    }
    location.href = id;
}

// 处理搜索框的搜索引擎切换事件
function handleChangeSearchPrefix(btn, prefix) {
    search_prefix = prefix;
    // 获取所有按钮元素
    const buttons = document.getElementById("btn-list").querySelectorAll("button");

    // 移除其他按钮的样式
    buttons.forEach(button => {
        button.classList.remove('active');
    });

    // 改变当前按钮的样式
    btn.classList.add('active');

    // 更新搜索框 placeholder
    if (btn.id === 'baidu'){
        document.getElementById("search-input").placeholder = '百度一下';
    }
    else if (btn.id === 'google'){
        document.getElementById("search-input").placeholder = 'Google两下';
    }
    else if (btn.id === 'bing'){
        document.getElementById("search-input").placeholder = '必应搜索';
    }
    else if (btn.id === 'sougou'){
        document.getElementById("search-input").placeholder = '搜狗搜索';
    }
    else if (btn.id === '360'){
        document.getElementById("search-input").placeholder = '360搜索';
    }
    else if (btn.id === 'toutiao'){
        document.getElementById("search-input").placeholder = '头条搜索';
    }

}