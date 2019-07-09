document.getElementById("test").addEventListener('click', () => {

    function getData() {
        var container = {};

        // division div varies across articles
        try {
          container["division"] = document.querySelector("#art-tags > a > span").innerText;
        } catch {
          try {
            container["division"] = document.querySelector("#art-tags > span").innerText;
          } catch {
            container["division"] = null
          }
        }

        // such as media type
        try {
          try {
            media = document.querySelector("#gazeta_article_image > div.article-image-photo > img")
            container["media_desc"] = media.alt;
            container["media_src"] = media.src;
            container["media_type"] = "image";
          } catch {
            media = document.querySelector("#gazeta_article_image > div.article-image-photo > a > img")
            container["media_desc"] = media.alt;
            container["media_src"] = media.src;
            container["media_type"] = "multiple_images";
          }
        } catch {
          try {
            container["media_desc"] = document.querySelector("#vjs_video_3 > div.vjs-title").innerText;
          } catch {
            container["media_desc"] = document.querySelector("#vjs_video_3_html5_api > div.vjs-title").innerText;
          }
          container["media_src"] = "";
          container["media_type"] = "video";
        }

        // also title
        try {
          container["title"] = document.querySelector("#art-header > div.art-headline > h1").innerText;
        } catch {
          container["title"] = document.querySelector("#pagetype_wideo > main > div > div > h1").innerText;
        }

        // author as well
        try {
          container["author"] = document.querySelector("#gazeta_article_author").innerText;
        } catch {
          container["author"] = document.querySelector("#art-header > div.art-header-meta > div.art-authors > span").innerText;
        }

        // same date
        try {
          container["date"] = document.querySelector("#art-datetime").innerText;
        } catch {
          container["date"] = document.querySelector("#gazeta_article_date").innerText;
        }

        // and highligh
        try {
          container["highlight"] = document.querySelector("#pagetype_art > div.content.container-inner > div.grid-row.splint-parent > section > article > section").innerText;
        } catch {
          container["highlight"] = document.querySelector("#pagetype_wideo > main > div > section > div.article > p").innerText;
        }

        console.log(container);
        return container;
    }

    //We have permission to access the activeTab, so we can call chrome.tabs.executeScript:
    chrome.tabs.executeScript({
        code: '(' + getData + ')();' //argument here is a string but function.toString() returns function's code
    }, (results) => {
        //Here we have just the innerHTML and not DOM structure
        console.log(results[0]);
    });
});
