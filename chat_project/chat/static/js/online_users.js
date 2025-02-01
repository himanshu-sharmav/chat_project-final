document.addEventListener('DOMContentLoaded', function() {
    const onlineSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/online/'
    );

    onlineSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type === 'online_users_update') {
            updateOnlineUsers(data.users);
        }
    };

    function updateOnlineUsers(users) {
        const usersList = document.getElementById('online-users-list');
        usersList.innerHTML = '';
        users.forEach(username => {
            usersList.innerHTML += `
                <div class="user-item">
                    <span class="online-indicator"></span>
                    ${username}
                </div>
            `;
        });
    }
}); 