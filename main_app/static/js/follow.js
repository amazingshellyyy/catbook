const handleFollow = () => {
	event.preventDefault();

	const element = event.target;
	const id = element.getAttribute('data-id');

	console.log(id);

	fetch(`/follow_user/${id}`, {
		method: 'GET',
	})
		.then(response => response.json())
		.then(data => {
			if (data.following) {
				element.innerHTML = 'Unfollow';
				element.style.opacity = '0.7';
			} else {
				element.innerHTML = 'Follow';
				element.style.opacity = '1';
			}
		})
		.catch(error => console.warn(error));
};

document.getElementById('followBtn').addEventListener('click', handleFollow);