<template>
    <div id="wrapper">
        <nav class="navbar is-dark">
            <div class="navbar-brand">
                <router-link to="/" class="navbar-item"><strong>ReadConnect</strong></router-link>
             </div>
            <div class="navbar-menu">
                <div class="navbar-end">
                    <template v-if="$store.state.isAuthenticated">
                        <router-link to="/dashboard/user_profile/" class="navbar-item">Dashboard</router-link>
                        <div class="navbar-item">
                            <div class="buttons">
                                 <router-link to="/dashboard/my-account/" class="button is-light">My Account</router-link>   
                            </div>
                        </div>
                     </template>
                     <template v-else>
                        <router-link to="/home" class="navbar-item">Home</router-link>
                        <div class="navbar-item">
                            <div class="buttons">
                                <router-link to="/sign-up/vue/" class="button is-success"><strong>Sign up</strong></router-link>
                                <router-link to="/login/vue/" class="button is-light"><strong>Login</strong></router-link>
                            </div>
                        </div>
                     </template>
                </div>
             </div>
        </nav>

        <section class="section">
            <router-view/>
        </section>

        <footer class="footer">
            <p class="hast-text-centered">@Copyright (c) 2023</p>
        </footer>
  </div>
</template>

<script>
    import axios from 'axios'
    import store from './store'; // Import your Vuex store
    export default {
        name: 'App',
        beforeCreate() {
            this.$store.commit("initializeStore");

            const token = this.$store.state.token;
            if (token) {
                axios.defaults.headers.common['Authorization'] = "Token " + token
            } else {
               axios.defaults.headers.common['Authorization'] = ""
            }
        }
    }
</script>
<style lang="scss">
    @import '../node_modules/bulma';
</style>
