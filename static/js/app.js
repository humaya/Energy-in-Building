$(function () {
    'use strict';
    const url = '/analysis/upload-csv';
    $('#fileupload').fileupload({
        url: url,
        method: "POST",
        dataType: 'json',
        done: function (e, data) {
            $("#progress").css(
                "display", "none"
            );
            const timeFormat = $("#time-format").val();
            const inputType = $("#input-type").val();
            console.log(timeFormat, inputType);

            data = data.result;
            const rbfData = [];
            const linData = [];
            const polyData = [];
            const energyData = [];
            const lrData = [];

            for (let i = 0; i < data.length; i++) {
                const time = new Date(data[i].parsedTime).getTime();
                rbfData.push([time, data[i].svr_rbf]);
                linData.push([time, data[i].svr_lin]);
                polyData.push([time, data[i].svr_poly]);
                lrData.push([time, data[i].lr]);
                energyData.push([time, data[i].energy]);
            }
            const series = [
                {
                    type: 'line',
                    name: 'SVR RBF',
                    data: rbfData
                },
                {
                    type: 'scatter',
                    name: 'Energy',
                    data: energyData
                }
            ];
            if (timeFormat !== "hourly") {
                series.push({
                    type: 'line',
                    name: 'SVR LIN',
                    data: linData
                });
                series.push({
                    type: 'line',
                    name: 'SVR POLY',
                    data: polyData
                })
            }
            if (inputType === "degree_day") {
                series.push({
                    type: 'line',
                    name: 'linear Regression',
                    data: lrData
                });
            }
            Highcharts.chart('chart', {
                    chart: {
                        zoomType: 'x'
                    },
                    title: {
                        text: 'Energy models in building'
                    },
                    subtitle: {
                        text: document.ontouchstart === undefined ?
                            'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                    },
                    xAxis: {
                        title: {
                            text: 'Time(day)'
                        },
                        type: 'datetime'
                    },
                    yAxis: {
                        title: {
                            text: 'Consumption(kWh)'
                        }
                    },
                    legend: {
                        enabled: true
                    },
                    plotOptions: {},

                    series: series

                }
            );
        },
        progressall: function (e, data) {
            const progress = parseInt(data.loaded / data.total * 100, 10);
            $("#progress").css(
                "display", "flex"
            );
            $('#progress .progress-bar').css(
                'width',
                progress + '%'
            );
        }
    }).bind('fileuploadsubmit', function (e, data) {
        data.formData = {
            timeFormat: $("#time-format").val(),
            inputType: $("#input-type").val()
        }
    })
        .prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');
});