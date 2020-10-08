Vue.component('l-map', window.Vue2Leaflet.LMap);
Vue.component('l-tile-layer', window.Vue2Leaflet.LTileLayer);
Vue.component('l-marker', window.Vue2Leaflet.LMarker);
Vue.component('l-circle-marker', window.Vue2Leaflet.LCircleMarker);
Vue.component('l-polyline', window.Vue2Leaflet.LPolyline);

Vue.component('mapper', {
    template: '#tested',
    props: ['service', 'busStops', 'busRoute'],
    data() {
        return {
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            zoom: 12,
            center: [1.3521, 103.8198],
        };
    },
    methods: {
        boundMapRects() {
            this.map = this.$refs.leafmap.mapObject;
            this.map.fitBounds(this.busRoute);
        },
    },
});

const app = new Vue({
    el: '#app',
});
