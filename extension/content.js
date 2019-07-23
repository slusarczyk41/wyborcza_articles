document.getElementById("content").addEventListener('click', () => {

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
            container["media"] = "image";
          } catch {
            media = document.querySelector("#gazeta_article_image > div.article-image-photo > a > img")
            container["media_desc"] = media.alt;
            container["media_src"] = media.src;
            container["media"] = "multiple_images";
          }
        } catch {
          try {
            container["media_desc"] = document.querySelector("#vjs_video_3 > div.vjs-title").innerText;
          } catch {
            container["media_desc"] = document.querySelector("#vjs_video_3_html5_api > div.vjs-title").innerText;
          }
          container["media_src"] = "";
          container["media"] = "video";
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

        container["content"] = document.querySelector("#pagetype_art > main > div > section > div.article.thin-article > article > section.article-text").innerText.replace(/(\r\n|\n|\r)/gm, "");

        return container

    }

    chrome.tabs.executeScript({
        code: '(' + getData + ')();'
    }, (container) => {
        var request = new XMLHttpRequest();
        request.open("POST", "http://127.0.0.1:5000", true);
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.send(JSON.stringify(container[0]));
        request.onreadystatechange = function() {
            if (request.readyState === 4){
                document.getElementById("results").innerHTML = request.response;
            } else {
                document.getElementById("results").innerHTML = 'Api is not working';
            }
        };

    });

});
