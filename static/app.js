Vue.component('l-map', window.Vue2Leaflet.LMap);
Vue.component('l-tile-layer', window.Vue2Leaflet.LTileLayer);
Vue.component('l-marker', window.Vue2Leaflet.LMarker);
Vue.component('l-circle-marker', window.Vue2Leaflet.LCircleMarker);
Vue.component('l-polyline', window.Vue2Leaflet.LPolyline);
Vue.component('l-tooltip', window.Vue2Leaflet.LTooltip);

Vue.component('mapper', {
    template: '#mapper',
    props: ['service', 'busStops', 'busRoute'],
    data() {
        return {
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            zoom: 12,
            center: [1.3521, 103.8198],
            marker: null,
        };
    },
    methods: {
        boundMapRects() {
            this.map = this.$refs.leafmap.mapObject;
            this.map.fitBounds(this.busRoute);
        },
        zoomAfterUpdate() {
            this.zoom = 20;
        },
    },
    created() {
        bus.$on('view_on_map', stop => {
            this.center = this.marker = [stop.lat, stop.lng];
            this.$refs.leafmap.$once('update:center', this.zoomAfterUpdate);
        });
    },
});

Vue.component('stop-map', {
    template: '#stop-map',
    props: ['stop', 'mark'],
    data() {
        return {
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            zoom: 20,
            center: this.mark,
            marker: this.mark,
        };
    },
    methods: {
        boundMapRects() {
            this.map = this.$refs.leafstopmap.mapObject;
        },
    },
});

Vue.component('bus-info', {
    template: '#bus-info',
    props: ['stops'],
    data() {
        return {
            isOpen: -1,
        };
    },
    methods: {
        opening(index) {
            this.isOpen = index;
            this.$emit('stop_carousel_open', index);
        },
    },
});

Vue.component('bus-info-panel', {
    template: '#bus-info-panel',
    props: ['stop', 'index'],
    data() {
        return {
            stopData: {},
        };
    },
    methods: {
        opened(openedIndex) {
            if (this.index !== openedIndex || !this.isEmpty()) {
                return;
            }

            axios.get(`/api/stop/${this.stop.stop_code}`).then(response => {
                this.stopData = response.data;
            });
        },
        isEmpty() {
            return Object.keys(this.stopData).length === 0;
        },
        viewOnMap() {
            bus.$emit('view_on_map', this.stop);
        },
    },
    created() {
        this.$parent.$parent.$on('stop_carousel_open', this.opened);
    },
});

Vue.component('bar-charty', {
    props: ['chartLabel', 'chartData', 'header'],
    extends: VueChartJs.Bar,
    data() {
        return {
            charting: {
                labels: this.chartLabel,
                datasets: [
                    {
                        label: this.header,
                        backgroundColor: '#f87979',
                        data: this.chartData,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    yAxes: [
                        {
                            ticks: {
                                beginAtZero: true,
                            },
                        },
                    ],
                },
            },
        };
    },
    mounted() {
        this.renderChart(this.charting, this.options);
    },
});

Vue.component('mall-traffic-info', {
    props: ['chartData', 'header'],
    extends: VueChartJs.Line,
    data() {
        return {
            charting: {
                labels: [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                datasets: [
                    {
                        label: this.header,
                        backgroundColor: '#f87979',
                        data: this.chartData,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                    xAxes: [
                        {
                            scaleLabel: {
                                display: true,
                                labelString: "Time of Day (Hour)"
                            }
                        },
                    ],
                    yAxes: [
                        {
                            scaleLabel: {
                                display: true,
                                labelString: "Volume of People"
                            },
                            ticks: {
                                beginAtZero: true,
                            },
                        },
                    ],
                },
            },
        };
    },
    mounted() {
        this.renderChart(this.charting, this.options);
    },
});

Vue.component('mall-traffic-info-second', {
    props: ['chartData', 'header'],
    extends: VueChartJs.Line,
    data() {
        return {
            charting: {
                labels: [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                datasets: [
                    {
                        label: this.header,
                        backgroundColor: '#f87979',
                        data: this.chartData,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    xAxes: [
                        {
                            scaleLabel: {
                                display: true,
                                labelString: "Time of Day (Hour)"
                            }
                        },
                    ],
                    yAxes: [
                        {
                            scaleLabel: {
                                display: true,
                                labelString: "Volume of People"
                            },
                            ticks: {
                                beginAtZero: true,
                            },
                        },
                    ],
                },
            },
        };
    },
    mounted() {
        this.renderChart(this.charting, this.options);
    },
});

Vue.component('mall-map', {
    template: '#mall-map',
    props: ['mark'],
    data() {
        return {
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            zoom: 20,
            center: this.mark,
            marker: this.mark,
        };
    },
    methods: {
        boundMapRects() {
            this.map = this.$refs.leafstopmap.mapObject;
        },
    },
});

Vue.component("day-type-selector", {
    template: '#toggle-day-type',
    data() {
        return {
            isWeekday: true
        }
    },
    methods: {
        toggleDayType() {
            this.isWeekday = !this.isWeekday;
            bus.$emit('changedDayType');

        }
    }
});

Vue.component("mall-graphs", {
    template: '#mall-graphs',
    data() {
        return {
            isWeekday: true
        }
    },
    created() {
        bus.$on('changedDayType', () => {
            this.isWeekday = !this.isWeekday;
        });
    }
});

Vue.component("mall-table", {
    template: '#mall-table',
    props: ['tableData'],
    data() {
        return {
            data: [],
            isBordered: true,
            isHoverable: true,
            sortIcon: 'arrow-up',
            sortIconSize: 'is-small',
            isStriped: true,
            isWeekday: true,
            obj: this.tableData
        }
    },
    watch: {
        isWeekday: function () {
            // Do something
            if (this.isWeekday) {
                this.data = this.obj["weekday"];
            } else {
                this.data = this.obj["weekend"];
            }
        }
    },
    created() {
        this.data = this.obj["weekday"];
        bus.$on('changedDayType', () => {
            this.isWeekday = !this.isWeekday;
        });
    }
});

Vue.component("mall-list-table", {
    template: '#mall-list-table',
    props: ['tableData'],
    data() {
        return {
            data: this.tableData,
            columns: [
                {
                    field: 'name',
                    label: 'Shopping Mall Name',
                    width: '500',
                    searchable: true,
                },
                {
                    field: 'url',
                    label: 'Link',
                    width: '500',
                }
            ],
            isBordered: false,
            isHoverable: true,
            isStriped: true
        }
    },
    mounted() {
        var mallsData = JSON.parse(JSON.stringify(this.data));
        var mallsArr = [];
        for (i = 0; i < this.data.length; i++)  {
            dict = {};
            var mallName = mallsData[i].name;
            var encodedName = encodeURI(mallName);

            dict.name = mallName;
            dict.url = "<a href='/mall/" + encodedName + "'>View Information</a>";

            mallsArr.push(dict);
        }
        this.data = mallsArr;
    }
});

const bus = new Vue();

const app = new Vue({
    el: '#app',
});
