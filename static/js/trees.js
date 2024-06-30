function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		const cookies = document.cookie.split(";");
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === name + "=") {
				cookieValue = decodeURIComponent(
					cookie.substring(name.length + 1)
				);
				break;
			}
		}
	}
	return cookieValue;
}

const csrftoken = getCookie("csrftoken");

function openCreateModal() {
	const createUrl = document
		.querySelector("[data-url-create]")
		.getAttribute("data-url-create");
	const form = document.getElementById("treeForm");
	form.action = createUrl;
	form.dataset.method = "post";
	document.getElementById("treeModalLabel").innerText = "Create Tree";
	form.reset();
}

function openUpdateModal(treeId) {
	axios
		.get(`/api/trees/planted-trees/${treeId}/`)
		.then((response) => {
			const tree = response.data;
			document.getElementById("treeModalLabel").innerText = "Update Tree";
			const form = document.getElementById("treeForm");
			form.action = `/api/trees/planted-trees/${treeId}/`;
			form.dataset.method = "put";
			document.getElementById("id_tree").value = tree.tree_id;
			document.getElementById("id_age").value = tree.age;
			document.getElementById("id_account").value = tree.account;
			document.getElementById("id_latitude").value = tree.latitude;
			document.getElementById("id_longitude").value = tree.longitude;
		})
		.catch((error) => {
			console.error("Error fetching tree data:", error);
			alert(
				"There was an error fetching the tree data. Please try again."
			);
		});
}

function deleteTree(treeId) {
	if (!confirm("Are you sure you want to delete this tree?")) return;

	axios({
		method: "delete",
		url: `/api/trees/planted-trees/${treeId}/`,
		headers: { "X-CSRFToken": csrftoken },
	})
		.then(() => refreshTreeList())
		.catch((error) => {
			console.error("Error deleting tree:", error);
			alert("There was an error deleting the tree. Please try again.");
		});
}

function handleSubmit(event) {
	event.preventDefault();
	const form = document.getElementById("treeForm");
	const formData = new FormData(form);

	const data = {
		age: formData.get("age"),
		account: formData.get("account"),
		latitude: parseFloat(formData.get("latitude")),
		longitude: parseFloat(formData.get("longitude")),
		tree_id: formData.get("tree"),
	};

	const url = form.action;
	const method = form.dataset.method;

	axios({
		method: method,
		url: url,
		data: JSON.stringify(data),
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": csrftoken,
		},
	})
		.then((response) => {
			if (response.status === 201 || response.status === 200) {
				const treeModal = document.getElementById("treeModal");
				const modal = bootstrap.Modal.getInstance(treeModal);
				modal.hide();

				form.reset();
				refreshTreeList();
			} else {
				alert("There was an error. Please try again.");
			}
		})
		.catch((error) => {
			console.error("Error submitting form:", error);
			alert("There was an error submitting the form. Please try again.");
		});
}

function createTreeItem(tree) {
	const treeItem = document.createElement("div");
	treeItem.className =
		"list-group-item list-group-item-action flex-column align-items-start";
	treeItem.setAttribute("data-id", tree.id);
	treeItem.innerHTML = `
        <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">${tree.tree.name} (${tree.tree.scientific_name})</h5>
        </div>
        <div class="d-flex flex-row align-items-center justify-content-between">
            <span>Age: ${tree.age}</span>
            <div>
                <a href="javascript:void(0);" class="btn btn-primary btn-sm" onclick="openDetailModal(${tree.id})">View Details</a>
                <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#treeModal" onclick="openUpdateModal(${tree.id})">Edit</button>
                <button class="btn btn-danger btn-sm" onclick="deleteTree(${tree.id})">Delete</button>
            </div>
        </div>
    `;
	return treeItem;
}

function openDetailModal(treeId) {
	axios
		.get(`/api/trees/planted-trees/${treeId}/`)
		.then((response) => {
			const tree = response.data;
			const modalBody = document.querySelector(
				"#treeDetailModal .modal-body"
			);
			modalBody.innerHTML = `
                <p><strong>Tree:</strong> ${tree.tree.name} (${
				tree.tree.scientific_name
			})</p>
                <p><strong>Age:</strong> ${tree.age}</p>
                <p><strong>Planted At:</strong> ${new Date(
					tree.planted_at
				).toLocaleString()}</p>
                <p><strong>Latitude:</strong> ${tree.latitude}</p>
                <p><strong>Longitude:</strong> ${tree.longitude}</p>
                <p><strong>Account ID:</strong> ${tree.account}</p>
            `;
			const detailModal = new bootstrap.Modal(
				document.getElementById("treeDetailModal")
			);
			detailModal.show();
		})
		.catch((error) => {
			console.error("Error fetching tree details:", error);
			alert(
				"There was an error fetching the tree details. Please try again."
			);
		});
}

function refreshTreeList(url = "/api/trees/planted-trees/") {
	axios
		.get(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
		.then((response) => {
			const treeList = document.getElementById("treeList");
			treeList.innerHTML = "";
			response.data.results.forEach((tree) =>
				treeList.appendChild(createTreeItem(tree))
			);

			const pagination = document.getElementById("pagination");
			pagination.innerHTML = "";

			if (response.data.previous) {
				const prevButton = document.createElement("button");
				prevButton.className = "btn btn-secondary";
				prevButton.innerText = "Previous";
				prevButton.onclick = () =>
					refreshTreeList(response.data.previous);
				pagination.appendChild(prevButton);
			}

			if (response.data.next) {
				const nextButton = document.createElement("button");
				nextButton.className = "btn btn-secondary";
				nextButton.innerText = "Next";
				nextButton.onclick = () => refreshTreeList(response.data.next);
				pagination.appendChild(nextButton);
			}
		})
		.catch((error) => {
			console.error("Error refreshing tree list:", error);
			alert(
				"There was an error refreshing the tree list. Please try again."
			);
		});
}

document.addEventListener("DOMContentLoaded", function () {
	const treeForm = document.getElementById("treeForm");
	treeForm.addEventListener("submit", handleSubmit);

	document
		.getElementById("treeModal")
		.addEventListener("hidden.bs.modal", () => {
			treeForm.reset();
			document
				.querySelectorAll(".modal-backdrop")
				.forEach((backdrop) => backdrop.remove());
		});

	refreshTreeList();
});
