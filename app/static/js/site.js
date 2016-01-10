(function(ragReport, $) {
    //Private Property
    var URL_SEP = '/';
    var report_NavParts = {};
    var report_NavQueryString = {};

    //Private Method
    function addPartToUrl(base, part){
        var ret_val = base;
        if (ret_val != null
        && ret_val.length > 0
        && ret_val.substr(ret_val.length - 1) != URL_SEP
        && part != null
        && part.length > 0
        && part.substr(0, 1) != URL_SEP) {
            ret_val += URL_SEP;
        }

        ret_val += part;

        return ret_val;
    }

    function keyIsNullOrInValues(obj, key, values){
        var ret = false;

        if (obj) {
            if (obj[key] == null) { ret = true; }

            if (values) {
                $.each(values, function (i, item) {
                    if (obj[key] == item) {
                        ret = true;
                    }
                });
            }
        }

        return ret;
    }

    //Public Property
    ragReport.defaultOptions = {};
    ragReport.defaultOptions.getDatePickerOptions = function(opt){
        var defaults = {
            showTodayButton: true,
            format: 'MM/DD/YYYY'
        };

        $.extend(defaults, opt || {});

        return defaults;
    };
    ragReport.defaultOptions.getDataTableOptions = function(opt){
        var defaults = {
        };

        $.extend(defaults, opt || {});

        return defaults;
    };

    ragReport.report = {};
    ragReport.report.NAV_HELPER_FROM = 'from';
    ragReport.report.NAV_HELPER_TO = 'to';
    ragReport.report.NAV_HELPER_URL_PART_1 = 'part_1';
    ragReport.report.NAV_HELPER_URL_PART_2 = 'part_2';
    ragReport.report.NAV_HELPER_URL_PART_3 = 'part_3';

    //Public Method
    ragReport.log = function(message){
        if (window.console){
            window.console.log(message);
        }
    };

    ragReport.warn = function(message){
        if (window.console){
            window.console.warn(message);
        }
    };

    ragReport.error = function(message){
        if (window.console){
            window.console.error(message);
        }
    };

    ragReport.report.setNavPart = function(key, value, callback){
        report_NavParts[key] = value;

        // Set the display if it's available
        if (callback){
            callback();
        }
    };

    ragReport.report.navToFilteredReport = function(){
        var base = window.location.origin;
        base = addPartToUrl(base, 'rag');

        /* Leaving my example.
        if (!keyIsNullOrInValues(report_NavParts, ragReport.report.NAV_HELPER_REPORT_TYPE, [''])) {
            base = addPartToUrl(base, report_NavParts[ragReport.report.NAV_HELPER_REPORT_TYPE]);
            if (!keyIsNullOrInValues(report_NavParts, ragReport.report.NAV_HELPER_REGION, ['', 'All'])) {
                base = addPartToUrl(base, report_NavParts[ragReport.report.NAV_HELPER_REGION]);
                if (!keyIsNullOrInValues(report_NavParts, ragReport.report.NAV_HELPER_CELL,['', 'All'])){
                    base = addPartToUrl(base, report_NavParts[ragReport.report.NAV_HELPER_CELL]);
                }
            }
        }
        */

        // Add from, to, step
        if (report_NavQueryString){
            var sep = '?';
            $.each(Object.keys(report_NavQueryString), function(i, item){
                base += sep + item + '=' + report_NavQueryString[item];
                sep = '&';
            });
        }

        window.location = base;
    };

    ragReport.report.seedNavHelper = function(){
        var base = window.location.href;
        var parts = base.split(URL_SEP);

        if (parts.length >= 4 && parts[4] != null && parts[4] != '' && parts[4].slice(0, 1) != '?'){
            ragReport.report.setNavPart(ragReport.report.NAV_HELPER_URL_PART_1, parts[4]);
        }else{
            ragReport.report.setNavPart(ragReport.report.NAV_HELPER_URL_PART_1, 'rag');
        }
        if (parts.length >= 5 && parts[5] != null && parts[5] != '' && parts[5].slice(0, 1) != '?'){
            ragReport.report.setNavPart(ragReport.report.NAV_HELPER_URL_PART_2, parts[5]);
            if (parts.length >= 6 && parts[6] != null && parts[6] != '' && parts[6].slice(0, 1) != '?'){
                ragReport.report.setNavPart(ragReport.report.NAV_HELPER_URL_PART_3, parts[6]);
            }
        }

        var split = base.split('?');
        if (split.length == 2) {
            var key_value = split[1].split('&');
            $.each(key_value, function(i, item){
                var parts = item.split('=');
                report_NavQueryString[parts[0]] = parts[1];
            });
        }
    };

    ragReport.report.setQueryParameterToUrl = function(key, value, callback){
        report_NavQueryString[key] = value;

        // Set the display if it's available
        if (callback){
            callback();
        }
    };
}( window.ragReport = window.ragReport || {}, jQuery ));