Vue.component('testing', {
    delimiters: ['!{', '}'],
    template: '#templ',
    data() {
        return {
            mmm: 'xd',
        };
    },
});

const app = new Vue({
    el: '#app',
    delimiters: ['!{', '}'],
});
