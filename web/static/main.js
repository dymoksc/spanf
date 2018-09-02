document.addEventListener('DOMContentLoaded', () => {
	const formsHtmlCollection = document.getElementsByTagName('form');

	Array.from(formsHtmlCollection)
		.filter(formElement => {
			return formElement.attributes.method.value === 'delete';
		})
		.forEach(formElement => {
			formElement.addEventListener('submit', e => {
				e.preventDefault();

				const xmlHttpRequest = new XMLHttpRequest();
				xmlHttpRequest.open('DELETE', formElement.attributes.action.value, true);
				xmlHttpRequest.onload = e => {
					if (xmlHttpRequest.readyState === 4 && xmlHttpRequest.status === 200) {
						location.reload();
					} else {
						console.error('Error on sending DELETE request', e, xmlHttpRequest);
					}
				};
				xmlHttpRequest.onerror = e => {
					console.error('Error on sending DELETE request', e, xmlHttpRequest);
				};
				xmlHttpRequest.send(null);
			});
		});
});
