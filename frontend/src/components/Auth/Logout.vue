<script>
export default {
    mounted() {
        localStorage.removeItem('tokens');
        this.$router.push('/login');
    }
}
</script>