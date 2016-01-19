      function toggleBlock(name) {
        var elem = document.getElementById(name);
        if(elem.style.display=='block') elem.style.display='none';
        else elem.style.display='block';
      }

      function showAbstracts() {
        var tags = document.getElementsByTagName('*');
        var newstyle;
        for(i=0,j=0; i<tags.length; i++) {
          if (tags[i].className.indexOf("abstract") != -1) {
            if(tags[i].style.display == "block") newstyle = "none";
            else newstyle = "block";
            break;
          }
        }
        for(i=0,j=0; i<tags.length; i++) {
        if (tags[i].className.indexOf("abstract") != -1)
          tags[i].style.display = newstyle;
        }
      }

      function hideBlocks() {
        var tags = document.getElementsByTagName('*');
        var newstyle;
        for(i=0,j=0; i<tags.length; i++) {
          if ((tags[i].className.indexOf("abstract") != -1) ||
              (tags[i].className.indexOf("bib") != -1) ||
              (tags[i].className.indexOf("sample") != -1)) {

              tags[i].style.display = "none";
          }
        }
      }
