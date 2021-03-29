// ==UserScript==
// @name         Rickroll Blocker
// @version      0.1
// @description  Block rickrolls for good
// @author       ch1ck3n / intelligente
// @match        *://*/*
// ==/UserScript==

(function () {
	'use strict';

	// Your code here...
	var checkurl = "https://rickroll-links-database.ch1ck3n.repl.co/yesorno/?url=";
	fetch(checkurl + location.href)
		.then(
			function (response) {
				// Examine the text in the response
				response.json().then(function (data) {
					if(data.data.rickroll == "True" && data.data.url != "repl.co"){
                     location.replace("https://rickroll-links-database.ch1ck3n.repl.co/bwah/?url=" + btoa(location.href))
                    }
				});
			}
		)
		.catch(function (err) {
			console.log('Fetch Error :-S', err);
		});
})();