      function english() {
        var tags = document.getElementsByTagName('*');
        for(i=0,j=0; i<tags.length; i++) {
          if (tags[i].className.indexOf("pt") != -1)
            tags[i].style.display="none";
          if (tags[i].className.indexOf("en") != -1)
            tags[i].style.display="block";
        }
        document.cookie = "vigusmaoLanguage=english"+"; path=/";
      }

      function portuguese() {
        var tags = document.getElementsByTagName('*');
        for(i=0,j=0; i<tags.length; i++) {
          if (tags[i].className.indexOf("en") != -1)
            tags[i].style.display="none";
          if (tags[i].className.indexOf("pt") != -1)
            tags[i].style.display="block";
        }
        document.cookie = "vigusmaoLanguage=portuguese"+"; path=/";
      }

      function readCookieLang() {
        if (document.cookie.indexOf("vigusmaoLanguage=english")>=0) return "english";
        if (document.cookie.indexOf("vigusmaoLanguage=portuguese")>=0) return "portuguese";
        return "";
      }

      function autoLanguage() {
        if (readCookieLang() == "english") english();
        else if(readCookieLang() == "portuguese") portuguese();
        else if(navigator.language.indexOf("pt")>=0) portuguese();
        else if(navigator.userLanguage.indexOf("pt")>=0) portuguese();
        else english();
      }
