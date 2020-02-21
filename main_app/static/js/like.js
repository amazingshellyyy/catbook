const handleLikes = () => {
	event.preventDefault();

	const element = event.target;

	if (!element) return;

	console.log(element.nodeName)
	const id = element.getAttribute('data-id');
	console.log(id);


	if(element.nodeName === "ION-ICON") {
		fetch(`/like_post/${id}`, {
			method: 'GET',
		})
			.then(response => response.json())
			.then(data => element.parentNode.innerHTML = `Like <ion-icon name="heart" style="position:relative;top:3px;" data-id="${id}"></ion-icon>${data}`)
			.catch(error => console.warn(error));

	} else if(element.nodeName === "A") {
		fetch(`/like_post/${id}`, {
			method: 'GET',
		})
			.then(response => response.json())
			.then(data => element.innerHTML = `Likes: <ion-icon name="heart" style="position:relative;top:3px;" data-id="${id}"></ion-icon>${data}`)
			.catch(error => console.warn(error));
	}
};

document.querySelectorAll('.like-btn').forEach(btn => btn.addEventListener('click', handleLikes));