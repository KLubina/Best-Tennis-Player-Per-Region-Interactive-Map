var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var landingpages;
(function (landingpages) {
    var sharing;
    (function (sharing) {
        var UtilFunctions = (function () {
            function UtilFunctions() {
            }
            UtilFunctions.bindEvent = function (target, event, method) {
                if (target.addEventListener) {
                    target.addEventListener(event, method, false);
                }
                else if (target['attachEvent']) {
                    target['attachEvent']('on' + event, method);
                }
            };
            UtilFunctions.unbindEvent = function (target, event, method) {
                if (target.removeEventListener) {
                    target.removeEventListener(event, method, false);
                }
                else if (target['detachEvent']) {
                    target['detachEvent']('on' + event, method);
                }
            };
            UtilFunctions.preventDefault = function (event) {
                event = event || window.event;
                if (event.preventDefault)
                    event.preventDefault();
                event.returnValue = false;
            };
            UtilFunctions.disableMouseWheel = function () {
                var _this = this;
                for (var i = 0; i < this.wheelEvents.length; i++)
                    this.bindEvent(window, this.wheelEvents[i], function (event) { return _this.preventDefault(event); });
            };
            UtilFunctions.enableMouseWheel = function () {
                var _this = this;
                for (var i = 0; i < this.wheelEvents.length; i++)
                    this.unbindEvent(window, this.wheelEvents[i], function (event) { return _this.preventDefault(event); });
            };
            UtilFunctions.extend = function (trgt, src) {
                for (var prop in src)
                    trgt[prop] = src[prop];
            };
            UtilFunctions.viewport = function () {
                var el = window, param = 'inner';
                if (!('innerWidth' in window)) {
                    el = document.documentElement || document.body;
                    param = 'client';
                }
                return { width: el["".concat(param, "Width")], height: el["".concat(param, "Height")] };
            };
            UtilFunctions.currentProtocol = function () {
                var re = /^https:/i, protocol = re.test(location.protocol) ? "https:" : "http:";
                if (document.getElementsByTagName) {
                    var baseElements = document.getElementsByTagName("base");
                    if (baseElements.length) {
                        var baseHref = baseElements[0].href;
                        if (baseHref && baseHref.length >= 6)
                            protocol = re.test(baseHref) ? "https:" : "http:";
                    }
                }
                return protocol;
            };
            UtilFunctions.wheelEvents = 'onwheel' in document || document.documentMode >= 9 ? ['wheel'] : ['mousewheel', 'DomMouseScroll', 'MozMousePixelScroll'];
            return UtilFunctions;
        }());
        sharing.UtilFunctions = UtilFunctions;
    })(sharing = landingpages.sharing || (landingpages.sharing = {}));
})(landingpages || (landingpages = {}));
var landingpages;
(function (landingpages) {
    var sharing;
    (function (sharing) {
        var Properties = (function () {
            function Properties(pageDomain, pageId, appearance, autoShow, keyDismiss, delay, showMobile, surveyWidth, transparent, shroudColor, shroudOpacity, attach, description) {
                if (attach === void 0) { attach = ""; }
                this.pageDomain = pageDomain;
                this.shroudColor = shroudColor;
                this.attach = attach;
                this.appearance = 0;
                this.autoShow = true;
                this.keyDismiss = false;
                this.delay = 0;
                this.showMobile = false;
                this.surveyWidth = 600;
                this.transparent = false;
                this.pageId = pageId.split('/')[0];
                if (appearance)
                    this.appearance = appearance === 'uc' ? 'uc' : parseInt(appearance);
                if (/false/i.test(autoShow))
                    this.autoShow = false;
                if (/true/i.test(keyDismiss))
                    this.keyDismiss = true;
                if (delay)
                    this.delay = parseInt(delay);
                if (/true/i.test(showMobile))
                    this.showMobile = true;
                if (surveyWidth)
                    this.surveyWidth = parseInt(surveyWidth) || this.surveyWidth;
                if (/true/i.test(transparent))
                    this.transparent = true;
                this.shroudOpacity = parseInt(shroudOpacity) || 0;
                this.description = description;
            }
            Properties.create = function (script) {
                if (/\?.*sharing=lp-/.test(script.src)) {
                    return this.createFromSrc(script.src);
                }
                else {
                    return this.createFromAttributes(script);
                }
            };
            Properties.createFromSrc = function (src) {
                var query = src.match(/\?(.+)#?/)[1].split(/&/), values = {};
                for (var i = 0; i < query.length; i++) {
                    var split = query[i].split(/=/);
                    if (split.length === 2)
                        values[split[0]] = decodeURIComponent(split[1]);
                }
                return this.parseAndCreate(values);
            };
            Properties.parseAndCreate = function (values) {
                return new Properties(values['domain'] || '', values['id'] || '', values['appearance'], values['auto'], values['keydismiss'], values['delay'], values['mobile'], values['width'], values['transparent'], values['shroudcolor'], values['shroudopacity'], values['attach'], values['description']);
            };
            Properties.createFromAttributes = function (script) {
                return new Properties(script.getAttribute('data-page-domain'), script.getAttribute('data-page-id'), script.getAttribute('data-appearance'), script.getAttribute('auto'), script.getAttribute('data-key-dismiss'), script.getAttribute('data-delay'), script.getAttribute('data-mobile'), null, null, null, null, null, null);
            };
            return Properties;
        }());
        sharing.Properties = Properties;
    })(sharing = landingpages.sharing || (landingpages.sharing = {}));
})(landingpages || (landingpages = {}));
var landingpages;
(function (landingpages) {
    var sharing;
    (function (sharing) {
        var SharingBase = (function () {
            function SharingBase(script) {
                this.script = script;
                this.sandbox = 'allow-modals allow-downloads allow-top-navigation allow-forms allow-same-origin allow-scripts allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation';
                this.properties = sharing.Properties.create(script);
                this.iframe = document.createElement('iframe');
                if (!window.ecPF)
                    window.ecPF = new landingpages.sharing.EmbeddingAPI(this.properties.pageDomain);
                window.ecPF._register(this, this.properties.pageId);
            }
            SharingBase.getScripts = function (selector) {
                return document.querySelectorAll("script[src*=\"sharing=lp-".concat(selector, "\"],script[data-sharing=lp-").concat(selector, "]"));
            };
            return SharingBase;
        }());
        sharing.SharingBase = SharingBase;
    })(sharing = landingpages.sharing || (landingpages.sharing = {}));
})(landingpages || (landingpages = {}));
var landingpages;
(function (landingpages) {
    var sharing;
    (function (sharing) {
        var EmbeddingAPI = (function () {
            function EmbeddingAPI(pageDomain) {
                var _this = this;
                this.pages = [];
                this.complete = [];
                window.lpXD.receiveMessage(function (msg) { return _this.messageRecieved(msg); }, landingpages.sharing.UtilFunctions.currentProtocol() + pageDomain);
            }
            EmbeddingAPI.prototype._register = function (form, pageId) {
                this.pages.push({ form: form, pageId: this.getId(pageId) });
            };
            EmbeddingAPI.prototype.messageRecieved = function (message) {
                var data = null;
                try {
                    data = JSON.parse(message.data);
                }
                catch (e) { }
                if (data && data.complete && data.name)
                    this.processComplete(data);
            };
            EmbeddingAPI.prototype.processComplete = function (data) {
                this.complete.filter(function (x) { return x.pageId === data.name || x.pageId === ''; }).forEach(function (x) { return x.method(data.formData); });
                if (data && data.formData && data.formData.contactEmail && window.dmPt) {
                    try {
                        window.dmPt('identify', data.formData.contactEmail);
                    }
                    catch (e) { }
                }
            };
            EmbeddingAPI.prototype.onComplete = function (fn, pageId) {
                if (pageId === void 0) { pageId = ''; }
                this.complete.push({ pageId: this.getId(pageId), method: fn });
            };
            EmbeddingAPI.prototype.open = function (pageId) {
                if (pageId === void 0) { pageId = ''; }
                this.getForms(pageId).forEach(function (x) { return x.form.open(); });
            };
            EmbeddingAPI.prototype.close = function (pageId) {
                if (pageId === void 0) { pageId = ''; }
                this.getForms(pageId).forEach(function (x) { return x.form.close(); });
            };
            EmbeddingAPI.prototype.getForms = function (name) {
                var _this = this;
                var forms = this.pages;
                if (name) {
                    forms = forms.filter(function (x) { return x.pageId === _this.getId(name); });
                }
                return forms;
            };
            EmbeddingAPI.prototype.getId = function (pageId) {
                return pageId.split('/')[0];
            };
            return EmbeddingAPI;
        }());
        sharing.EmbeddingAPI = EmbeddingAPI;
    })(sharing = landingpages.sharing || (landingpages.sharing = {}));
})(landingpages || (landingpages = {}));
var landingpages;
(function (landingpages) {
    var sharing;
    (function (sharing) {
        if (!window.lpXD) {
            window.lpXD = function () {
                var interval_id, last_hash, cache_bust = 1, attached_callback, window = this;
                return {
                    postMessage: function (message, target_url, target) {
                        if (!target_url) {
                            return;
                        }
                        target = target || parent;
                        if (/dsid=/.test(location.search)) {
                            var dsid = location.search.replace(/.*dsid=([^&]+)/, '$1');
                            message = message.replace(/\}\s*$/, ",\"islpsurvey\":true, \"dsid\":\"".concat(dsid, "\"}"));
                        }
                        if (window['postMessage']) {
                            target['postMessage'](message, target_url.replace(/([^:]+:\/\/[^\/]+).*/, '$1'));
                        }
                        else if (target_url) {
                            target.location = target_url.replace(/#.*$/, '') + '#' + (+new Date) + (cache_bust++) + '&' + message;
                        }
                    },
                    receiveMessage: function (callback, source_origin) {
                        if (window['postMessage']) {
                            if (callback) {
                                attached_callback = function (e) {
                                    if ((Object.prototype.toString.call(source_origin) === "[object Function]" && source_origin(e.origin) === !1)) {
                                        return !1;
                                    }
                                    callback(e);
                                };
                            }
                            if (window['addEventListener']) {
                                window[callback ? 'addEventListener' : 'removeEventListener']('message', attached_callback, !1);
                            }
                            else {
                                window[callback ? 'attachEvent' : 'detachEvent']('onmessage', attached_callback);
                            }
                        }
                        else {
                            interval_id && clearInterval(interval_id);
                            interval_id = null;
                            if (callback) {
                                interval_id = setInterval(function () {
                                    var hash = document.location.hash, re = /^#?\d+&/;
                                    if (hash !== last_hash && re.test(hash)) {
                                        last_hash = hash;
                                        callback({ data: hash.replace(re, '') });
                                    }
                                }, 100);
                            }
                        }
                    }
                };
            }();
        }
    })(sharing = landingpages.sharing || (landingpages.sharing = {}));
})(landingpages || (landingpages = {}));
var landingpages;
(function (landingpages) {
    var sharing;
    (function (sharing) {
        var CookieManager = (function () {
            function CookieManager(id) {
                this.completeName = "".concat(id, "-Completed");
                this.dismissedName = "".concat(id, "-Dismissed");
            }
            CookieManager.prototype.read = function (name) {
                var nameEQ = "".concat(name, "="), cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i];
                    while (cookie.charAt(0) === ' ')
                        cookie = cookie.substring(1, cookie.length);
                    if (cookie.indexOf(nameEQ) === 0)
                        return cookie.substring(nameEQ.length, cookie.length);
                }
                return null;
            };
            CookieManager.prototype.write = function (name, value, days) {
                var expires = "";
                if (days) {
                    var date = new Date();
                    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                    expires = "; expires=".concat(date.toUTCString());
                }
                document.cookie = "".concat(name, "=").concat(value).concat(expires, ";secure=true; path=/");
            };
            CookieManager.prototype.clear = function (name) {
                document.cookie = "".concat(name, "=;secure=true; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;");
            };
            return CookieManager;
        }());
        sharing.CookieManager = CookieManager;
    })(sharing = landingpages.sharing || (landingpages.sharing = {}));
})(landingpages || (landingpages = {}));
var landingpages;
(function (landingpages) {
    var sharing;
    (function (sharing) {
        var EmbedCookieManager = (function () {
            function EmbedCookieManager(pageId) {
                this.pageId = pageId;
                this.cookieManager = new sharing.CookieManager(this.pageId);
            }
            EmbedCookieManager.prototype.setCompletedCookie = function () {
                this.cookieManager.write(this.cookieManager.completeName, 'true', 365);
            };
            EmbedCookieManager.prototype.hasBeenCompleted = function () {
                return this.cookieManager.read(this.cookieManager.completeName) == 'true';
            };
            return EmbedCookieManager;
        }());
        sharing.EmbedCookieManager = EmbedCookieManager;
    })(sharing = landingpages.sharing || (landingpages.sharing = {}));
})(landingpages || (landingpages = {}));
var landingpages;
(function (landingpages) {
    var sharing;
    (function (sharing) {
        var SharingEmbed = (function (_super) {
            __extends(SharingEmbed, _super);
            function SharingEmbed(script) {
                var _this = _super.call(this, script) || this;
                _this.script = script;
                if (window.__dmProcessedPages.indexOf(_this.properties.pageId) > -1)
                    return _this;
                window.__dmProcessedPages.push(_this.properties.pageId);
                _this.cookieManager = new sharing.EmbedCookieManager(_this.properties.pageId);
                if (_this.properties.autoShow)
                    _this.open();
                window.lpXD.receiveMessage(function (msg) {
                    try {
                        var message = JSON.parse(msg.data);
                        if (message.name === _this.properties.pageId) {
                            if (message.complete)
                                _this.cookieManager.setCompletedCookie();
                            if (message.height)
                                _this.setHeight(message.height.toString());
                        }
                    }
                    catch (e) { }
                }, sharing.UtilFunctions.currentProtocol() + _this.properties.pageDomain);
                return _this;
            }
            SharingEmbed.create = function () {
                window.__dmProcessedPages = window.__dmProcessedPages || [];
                var scripts = _super.getScripts.call(this, 'embed');
                for (var i = 0; i < scripts.length; i++)
                    new SharingEmbed(scripts[i]);
            };
            SharingEmbed.prototype.open = function () {
                this.setAttributes();
                var attach = this.properties.attach ? document.querySelector(this.properties.attach) : null;
                if (!attach)
                    attach = this.script.parentElement;
                attach.appendChild(this.iframe);
            };
            SharingEmbed.prototype.close = function () {
                this.iframe.parentNode.removeChild(this.iframe);
            };
            SharingEmbed.prototype.setAttributes = function () {
                var completed = this.cookieManager.hasBeenCompleted() ? '/?__lpcomplete=true' : '';
                this.iframe.setAttribute('src', "//".concat(this.properties.pageDomain, "/p/").concat(this.properties.pageId).concat(completed, "#").concat(document.location.href));
                this.iframe.setAttribute('id', this.properties.pageId);
                this.iframe.setAttribute('class', '_lpSurveyEmbed');
                this.iframe.setAttribute('name', this.properties.pageId);
                this.iframe.setAttribute('width', '100%');
                this.iframe.setAttribute('frameborder', '0');
                this.iframe.setAttribute('scrolling', 'no');
                this.iframe.setAttribute('allow', 'geolocation');
                this.iframe.setAttribute('sandbox', this.sandbox);
                this.iframe.setAttribute('style', SharingEmbed.baseStyle);
                if (this.properties.description) {
                    this.iframe.setAttribute('title', this.properties.description);
                }
                this.script.setAttribute('data-iframe-loaded', 'true');
            };
            SharingEmbed.prototype.setHeight = function (height) {
                this.iframe.setAttribute('height', height);
                this.iframe.setAttribute('max-height', height);
            };
            SharingEmbed.openned = [];
            SharingEmbed.baseStyle = 'border:none 0!important;margin:0!important;padding:0!important;';
            return SharingEmbed;
        }(sharing.SharingBase));
        SharingEmbed.create();
    })(sharing = landingpages.sharing || (landingpages.sharing = {}));
})(landingpages || (landingpages = {}));
