const handleLikes = () => {
	event.preventDefault();

	const element = event.target;
	const id = event.target.getAttribute('data-id');
	console.log(id);

	fetch(`/like_post/${id}`, {
		method: 'GET',
	})
		.then(response => response.json())
		.then(data => element.innerHTML = `Likes: ${data}`)
		.catch(error => console.warn(error));
};

document.querySelectorAll('.like-btn').forEach(btn => btn.addEventListener('click', handleLikes));