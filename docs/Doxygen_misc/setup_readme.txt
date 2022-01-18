To set default toggle level on files tab, paste this script to the end of files.html:
<script type="text/javascript">
if(window.location.href.indexOf('files.html') >= 0)
{   toggleLevel(2);
}
</script>
