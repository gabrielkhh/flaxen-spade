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
    },
    created() {
        bus.$on('view_on_map', stop => {
            this.center = this.marker = [stop.lat, stop.lng];
            this.zoom = 20;
        });
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

Vue.component('charty', {
    extends: VueChartJs.Bar,
    data() {
        return {
            charting: {
                labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                datasets: [
                    {
                        label: 'バスどこ',
                        backgroundColor: '#f87979',
                        data: [12, 19, 3, 5, 2, 3],
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

const bus = new Vue();

const app = new Vue({
    el: '#app',
});
