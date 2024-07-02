function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		const cookies = document.cookie.split(";");
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.startsWith(name + "=")) {
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
const currentUser = document.getElementById("currentUser").dataset.username;

function openCreateModal() {
	const createUrl = document
		.querySelector("[data-url-create]")
		.getAttribute("data-url-create");
	const form = document.getElementById("accountForm");
	form.action = createUrl;
	form.dataset.method = "post";
	document.getElementById("accountModalLabel").innerText = "Create Account";
	form.reset();
}

async function openUpdateModal(accountId) {
	try {
		const response = await axios.get(`/api/accounts/${accountId}/`);
		const account = response.data;
		document.getElementById("accountModalLabel").innerText =
			"Update Account";
		const form = document.getElementById("accountForm");
		form.action = `/api/accounts/${accountId}/`;
		form.dataset.method = "put";
		document.getElementById("id_name").value = account.name;
		document.getElementById("id_active").checked = account.active;
	} catch (error) {
		alert(
			"There was an error fetching the account data. Please try again."
		);
		console.error("Error fetching account data:", error);
	}
}

function createAccountItem(account) {
	const accountItem = document.createElement("div");
	accountItem.className =
		"list-group-item list-group-item-action flex-column align-items-start";
	accountItem.setAttribute("data-id", account.id);
	let buttons = "";

	if (account.created_by === currentUser) {
		buttons = `
			<button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#accountModal" onclick="openUpdateModal(${account.id})">Edit</button>
			<button class="btn btn-danger btn-sm" onclick="deleteAccount(${account.id})">Delete</button>
		`;
	}

	accountItem.innerHTML = `
		<div class="d-flex w-100 justify-content-between">
			<h5 class="mb-1">${account.name}</h5>
		</div>
		<div class="d-flex flex-row align-items-center justify-content-between">
			<span>${account.active ? "Active" : "Inactive"}</span>
			<div>
				${buttons}
			</div>
		</div>
	`;
	return accountItem;
}

async function refreshAccountList(filter = "member", url = "/api/accounts/") {
	try {
		const response = await axios.get(url, {
			params: { filter_by: filter },
			headers: { "x-requested-with": "XMLHttpRequest" },
		});

		const accountList = document.getElementById("accountList");
		accountList.innerHTML = "";

		if (response.data.results.length === 0) {
			const noAccountsMessage = document.createElement("div");
			noAccountsMessage.className = "list-group-item";
			noAccountsMessage.innerText = "No accounts found.";
			accountList.appendChild(noAccountsMessage);
		} else {
			response.data.results.forEach((account) =>
				accountList.appendChild(createAccountItem(account))
			);
		}

		const pagination = document.getElementById("pagination");
		pagination.innerHTML = "";

		if (response.data.previous) {
			const prevButton = document.createElement("button");
			prevButton.className = "btn btn-secondary";
			prevButton.innerText = "Previous";
			prevButton.onclick = () =>
				refreshAccountList(filter, response.data.previous);
			pagination.appendChild(prevButton);
		}

		if (response.data.next) {
			const nextButton = document.createElement("button");
			nextButton.className = "btn btn-secondary";
			nextButton.innerText = "Next";
			nextButton.onclick = () =>
				refreshAccountList(filter, response.data.next);
			pagination.appendChild(nextButton);
		}
	} catch (error) {
		console.error("Error fetching account list:", error);
		alert(
			"There was an error refreshing the account list. Please try again."
		);
	}
}

async function handleSubmit(event) {
	event.preventDefault();
	const form = document.getElementById("accountForm");
	const formData = new FormData(form);
	const url = form.action;
	const method = form.dataset.method;

	try {
		const response = await axios({
			method: method,
			url: url,
			data: formData,
			headers: {
				"Content-Type": "multipart/form-data",
				"X-CSRFToken": csrftoken,
			},
		});

		if (response.data.id) {
			const accountModal = document.getElementById("accountModal");
			const modal = bootstrap.Modal.getInstance(accountModal);
			modal.hide();

			document.body.classList.remove("modal-open");
			document
				.querySelectorAll(".modal-backdrop")
				.forEach((backdrop) => backdrop.remove());

			form.reset();
			refreshAccountList();
		} else {
			alert("There was an error. Please try again.");
		}
	} catch (error) {
		alert("There was an error submitting the form. Please try again.");
		console.error("Error submitting the form:", error);
	}
}

async function deleteAccount(accountId) {
	if (confirm("Are you sure you want to delete this account?")) {
		try {
			await axios({
				method: "delete",
				url: `/api/accounts/${accountId}/`,
				headers: {
					"X-CSRFToken": csrftoken,
				},
			});
			refreshAccountList();
		} catch (error) {
			alert("There was an error deleting the account. Please try again.");
			console.error("Error deleting the account:", error);
		}
	}
}

function applyFilter(filterType) {
	refreshAccountList(filterType);
}

document.addEventListener("DOMContentLoaded", function () {
	const accountForm = document.getElementById("accountForm");
	accountForm.addEventListener("submit", handleSubmit);

	document
		.getElementById("accountModal")
		.addEventListener("hidden.bs.modal", () => {
			accountForm.reset();
			document
				.querySelectorAll(".modal-backdrop")
				.forEach((backdrop) => backdrop.remove());
		});

	refreshAccountList();
});
