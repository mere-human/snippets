// open post and paste it to the developer console
var printVideos = function () {
    let videoUrls = new Set();
    let collectVideos = function (className) {
        let maxIters = 20;
        for (let i = 0; i != maxIters; ++i) {
            let videoElems = document.querySelectorAll('video');
            for (let j = 0; j != videoElems.length; ++j)
                videoUrls.add(videoElems[j].src);
            let buttonElems = document.querySelectorAll('button div[class*="' + className + '"]');
            if (!buttonElems || buttonElems.length <= 0)
                break;
            buttonElems[0].parentElement.click();
        }
    };
    collectVideos('coreSpriteRightChevron');
    collectVideos('coreSpriteLeftChevron');
    console.log('===== Videos: ==================');
    videoUrls.forEach(function (value) {
        console.log(value)
    });
    console.log('================================')
}();