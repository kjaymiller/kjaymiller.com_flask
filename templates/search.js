<script src="https://cdn.jsdelivr.net/npm/fuse.js@6.0.0"></script>
<script type="text/javascript">

const options = {
  // isCaseSensitive: false,
  // includeScore: false,
  // shouldSort: true,
  // includeMatches: false,
  // findAllMatches: false,
  // minMatchCharLength: 1,
  // location: 0,
  // threshold: 0.6,
  // distance: 100,
  // useExtendedSearch: false,
};

fetch('/search.json')
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    const fuse = new Fuse(data, options);
    return fuse
  })
  .catch(function (err) {
    console.log(err);
  });


</script>
