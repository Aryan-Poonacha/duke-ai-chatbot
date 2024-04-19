/*jshint browser:true */
/*!
* FitVids 1.1
*
* Copyright 2013, Chris Coyier - http://css-tricks.com + Dave Rupert - http://daverupert.com
* Credit to Thierry Koblentz - http://www.alistapart.com/articles/creating-intrinsic-ratios-for-video/
* Released under the WTFPL license - http://sam.zoy.org/wtfpl/
*
*/

;(function( $ ){

  'use strict';

  $.fn.fitVids = function( options ) {
    var settings = {
      customSelector: null,
      ignore: null
    };

    if(!document.getElementById('fit-vids-style')) {
      // appendStyles: https://github.com/toddmotto/fluidvids/blob/master/dist/fluidvids.js
      var head = document.head || document.getElementsByTagName('head')[0];
      var css = '.fluid-width-video-wrapper{width:100%;position:relative;padding:0;}.fluid-width-video-wrapper iframe,.fluid-width-video-wrapper object,.fluid-width-video-wrapper embed {position:absolute;top:0;left:0;width:100%;height:100%;}';
      var div = document.createElement("div");
      div.innerHTML = '<p>x</p><style id="fit-vids-style">' + css + '</style>';
      head.appendChild(div.childNodes[1]);
    }

    if ( options ) {
      $.extend( settings, options );
    }

    return this.each(function(){
      var selectors = [
        'iframe[src*="player.vimeo.com"]',
        'iframe[src*="youtube.com"]',
        'iframe[src*="youtube-nocookie.com"]',
        'iframe[src*="kickstarter.com"][src*="video.html"]',
        'object',
        'embed',
        'iframe[src*="google.com"]'
      ];

      if (settings.customSelector) {
        selectors.push(settings.customSelector);
      }

      var ignoreList = '.fitvidsignore';

      if(settings.ignore) {
        ignoreList = ignoreList + ', ' + settings.ignore;
      }

      var $allVideos = $(this).find(selectors.join(','));
      $allVideos = $allVideos.not('object object'); // SwfObj conflict patch
      $allVideos = $allVideos.not(ignoreList); // Disable FitVids on this video.

      $allVideos.each(function(){
        var $this = $(this);
        if($this.parents(ignoreList).length > 0) {
          return; // Disable FitVids on this video.
        }
        if (this.tagName.toLowerCase() === 'embed' && $this.parent('object').length || $this.parent('.fluid-width-video-wrapper').length) { return; }
        if ((!$this.css('height') && !$this.css('width')) && (isNaN($this.attr('height')) || isNaN($this.attr('width'))))
        {
          $this.attr('height', 9);
          $this.attr('width', 16);
        }
        var height = ( this.tagName.toLowerCase() === 'object' || ($this.attr('height') && !isNaN(parseInt($this.attr('height'), 10))) ) ? parseInt($this.attr('height'), 10) : $this.height(),
            width = !isNaN(parseInt($this.attr('width'), 10)) ? parseInt($this.attr('width'), 10) : $this.width(),
            aspectRatio = height / width;
        if(!$this.attr('name')){
          var videoName = 'fitvid' + $.fn.fitVids._count;
          $this.attr('name', videoName);
          $.fn.fitVids._count++;
        }
        $this.wrap('<div class="fluid-width-video-wrapper"></div>').parent('.fluid-width-video-wrapper').css('padding-top', (aspectRatio * 100)+'%');
        $this.removeAttr('height').removeAttr('width');
      });
    });
  };
  
  // Internal counter for unique video names.
  $.fn.fitVids._count = 0;
  
// Works with either jQuery or Zepto
})( window.jQuery || window.Zepto );
;/*})'"*/;/*})'"*/
/**
 * @file
 * A JavaScript file for the theme.
 *
 * In order for this JavaScript to be loaded on pages, see the instructions in
 * the README.txt next to this file.
 */

// JavaScript should be made compatible with libraries other than jQuery by
// wrapping it with an "anonymous closure". See:
// - https://drupal.org/node/1446420
// - http://www.adequatelygood.com/2010/3/JavaScript-Module-Pattern-In-Depth
(function ($, Drupal, window, document, undefined) {


// To understand behaviors, see https://drupal.org/node/756722#behaviors
	Drupal.behaviors.my_custom_behavior = {
		
		attach: function(context, settings) {

			/*START ACCORDION*/
			//Hide panels 
			$(".accordion >div").hide();
			$(".accordionView .views-row >div").hide();
     	 	$(".accordionContent.view-faculty .view-content >div").hide();
  
			//Show default panel if it exists
			$(".accordion .default").addClass("current").next("div").slideToggle();
  
			//When a heading is clicked
			$(".accordion").find(">h2,>h3,>h4,>h5,>h6,>p").click(function(){
	
				//Show selected panel and hide other panels
				$(this).next("div").slideToggle().siblings("div:visible").slideUp();
	
				//Add or remove class
				$(this).toggleClass("current");
	
				//Remove class from other headings
				$(this).siblings("h2,h3,h4,h5,h6,p").removeClass("current");
			});
			

			//Accordions used in VIEWS
			$(".accordionView .views-row").find(".toggle").click(function(e) {
				e.preventDefault();

				var $this = $(this);

				if ($this.hasClass("current")) {
				$this.toggleClass("current");
				$this.next().slideToggle();
				} else {
				$this.parent().parent().find(".views-row > .toggle").removeClass("current");
				$this.parent().parent().find(".views-row > div").slideUp();
				$this.toggleClass("current");
				$this.next().slideToggle();
				}

			});
      

			//Accordion used in ECE faculty view - MD - changed so toggle is flagged current
			
			//When a heading is clicked
      $(".accordionContent.view-faculty").find(".toggle").click(function(e){

        e.preventDefault();

        //Show selected panel and hide other panels
        $(this).next("div").slideToggle().siblings("div:visible").slideUp();
	
        //Add or remove class
        $(this).toggleClass("current");
	
        //Remove class from other headings
        $(this).siblings(".toggle").removeClass("current");
      });
      
      
      //Fancy Accordions - MF
      $('.accordion2021').each(function () {
        var $accordion = $(this);
        $accordion.find('span.accordion-button').click(function () {
          // Change false to true and back.
          var $button = $(this);
          var $ariaExpanded = $button.attr('aria-expanded');
          var $id = $button.attr('aria-controls');
          if ($ariaExpanded === 'true') {
            $button.attr('aria-expanded', 'false');
          }
          else {
            $button.attr('aria-expanded', 'true');
          }
          $accordion.find('#' + $id).toggle();
        });
      });


      /*END VIEW ACCORDION*/
      
			
            
			/*START FITVIDS*/
			//http://fitvidsjs.com - responsive resizing of videos
    		// Target your .container, .wrapper, .post, etc.
    		$("#main").fitVids();
			/*END FITVIDS*/
			
			/*START TABLE SCROLL*/
			$( "#main #content table" ).wrap( "<div class='table'></div>" );
			/*END TABLE SCROLL*/
	  
	  
	  		/*FIX SIDEBAR MENU ACTIVE-TRAIL ISSUE*/
			$('#sidebar-navigation.block li.active').siblings('li.active-trail').removeClass('active-trail');
			/*END SIDEBAR MENU FIX*/
	  		
			  /*THIS FUNCTIONALITY WAS REPLACED BY THE MENU_TRAIL_BY_PATH MODULE*/
			  //Check to see if node-type is faculty and add active-trail class to menu item
			  /*if($("body").hasClass("node-type-faculty")) {
				var active = document.getElementById("menu-link-faculty").parentNode;
				active.className += " active-trail";
			  }
	  
			  //Check to see if node-type is Duke Calendar Event and add active-trail class to menu item
			  if($("body").hasClass("node-type-duke-calendar") || $("body").hasClass("node-type-grad-seminar")) {
				var active = document.getElementById("menu-link-about").parentNode;
				active.className += " active-trail";
				var subActive = document.getElementByID("menu-link-events").parentNode;
				subActive.className += " active-trail";
			  }

			  //If grad student seminar, add active-trail to menu item
			  /*if($("body").hasClass("node-type-grad-seminar")) {
				var active = document.getElementById("menu-link-about").parentNode;
				active.className += " active-trail";
			  }*/
	  
			  //If news story, add active-trail class to menu item
			  /*if($("body").hasClass("page-about-news-")) {
				var active = document.getElementById("menu-link-about").parentNode;
				active.className += " active-trail";
			  }*/

			  /*Add a class to the #hero parent of .overlap for better control of styling*/
			  $('#block-views-field-display-hero-image').parent('#hero').addClass('heroOverlap');


    // FRONT PAGE HERO

	if($('body.front').length) {
		var defaultBody = $('#tabs span.tab').first().attr("data-body");
		var defaultAlt = $('#tabs span.text').first().text();
		var defaultTabid = $('#tabs span.tab').first().attr("default-background");
		var defaultStyle = $('#tabs span.tab').first().attr("data-style");
		var defaultClass = $('#tabs span.tab').first().attr("data-class");
		var allClass = 'banner active ' + defaultTabid + ' ' + defaultClass ;

		$("#hero-home #default div.layout").replaceWith( defaultBody );
		$("#hero-home #default.banner").attr('alt', $.trim(defaultAlt));
		$("#hero-home #default.banner").attr('style', $.trim(defaultStyle));
		$("#hero-home #default").attr('class', allClass  );

		$('#tabs span.tab').first().addClass('active');

	};

	$("body.front .tab").on("click", function() { // Toggle between hero images, when tab icon is clicked
		var vBody = $( this ).attr("data-body");
		var vTxt = $( this, '.span.text').text();
		var vTabid = $( this ).attr("default-background");
		var vStyles = $( this ).attr("data-style");
		var vClass =  $( this ).attr("data-class");
		var vClasses = 'banner active ' + vClass + ' ' + vTabid; 

		$(".tab").removeClass("active");
		$(this).addClass("active");
		$(this).click(false);

		$("#hero-home .banner#default").attr('class', vClasses );
		$("#hero-home .banner#default div").addClass( vTabid );
		$("#hero-home #default div").replaceWith( vBody );
		$("#hero-home .banner#default").attr('alt', $.trim( vTxt));
		$("#hero-home .banner#default").attr('style', ( vStyles ));

	}); // END FRONT PAGE HERO

			
			/*FIX FOR ECE FACULTY SORT*/

			//Add allFaculty class on load since this is the default.
			$('div.view-display-id-ece_faculty div.view-content').addClass('allFaculty');
			
			//After the Ajax executes when a radio button is clicked
			$(document).ajaxComplete(function() {

				//Get value of the selected button
				var radioValue = $("div.view-display-id-ece_faculty input[name='taxonomy_vocabulary_4_tid']:checked").val();

				//If the value is not 'all', change class to researchFilter
				if(radioValue != 'All') {
					$('div.view-display-id-ece_faculty div.view-content').attr('class', 'view-content researchFilter');
				};			
			})
		}
	};
})(jQuery, Drupal, this, this.document);
;/*})'"*/;/*})'"*/
