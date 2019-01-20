window.addEventListener('load', function () {
    firebase.auth().onAuthStateChanged(function (user) {
        if (user) { // User signed in
            console.log(`Signed in as ${user.displayName} (${user.email})`);
            user.getIdToken().then(function (token) {
                // Only put the token in the cookie (security)
                document.cookie = "token=" + token;
            });

            var welcome = document.getElementById('welcome');
            if(welcome) {
                welcome.innerHTML = 'Welcome, ' + user.displayName;
                console.log('Welcome, ' + user.displayName);
            }
        } else { // User signed out
            document.cookie = "token=";
        }
    }, function (error) {
        console.log(error);
        alert('Unable to log in: ' + error);
    });
});
