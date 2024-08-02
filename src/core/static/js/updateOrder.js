import { API } from "./api.js";

function updateSummary() {
  let total = 0;
  const selectedCertificates = document.querySelectorAll(
    '#list-certificates input[type="checkbox"]:checked'
  );
  const selectedFees = document.querySelectorAll(
    '#list-fees input[type="checkbox"]:checked'
  );

  selectedCertificates.forEach((item) => {
    const price = parseFloat(item.dataset.price);
    console.log(`Selected certificate: ${item.value}, Price: ${price}`);
    total += price;
  });

  selectedFees.forEach((item) => {
    const price = parseFloat(item.dataset.price);
    console.log(`Selected fee: ${item.name}, Price: ${price}`);
    total += price;
  });

  console.log(`Total calculated: ${total}`);

  const summaryElement = document.getElementById("order-summary");
  if (summaryElement) {
    summaryElement.textContent = `Total: $${total.toFixed(2)}`;
  }
}

function createOrder() {
  const selectedCertificates = Array.from(
    document.querySelectorAll(
      '#list-certificates input[type="checkbox"]:checked'
    )
  ).map((checkbox) => ({
    certificate_id: parseInt(checkbox.value),
    fee_id: null,
  }));

  const selectedFees = Array.from(
    document.querySelectorAll('#list-fees input[type="checkbox"]:checked')
  ).map((checkbox) => parseInt(checkbox.value));

  // Assign fees to certificates
  for (let i = 0; i < selectedCertificates.length; i++) {
    if (i < selectedFees.length) {
      selectedCertificates[i].fee_id = selectedFees[i];
    }
  }

  const data = {
    property_id: 1,
    lines: selectedCertificates,
  };

  console.log("Data being sent to server:", data);

  API.createOrderSession(data)
    .then((data) => {
      if (data.success && data.checkout_url) {
        window.location.href = data.checkout_url;
      } else {
        throw new Error(data.error || "Unknown error");
      }
    })
    .catch((error) => {
      console.error("Error creating order:", error);
      alert("An error occurred while creating the order.");
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const checkboxes = document.querySelectorAll(
    '#list-certificates input[type="checkbox"], #list-fees input[type="checkbox"]'
  );
  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", updateSummary);
  });

  updateSummary();

  const continueButton = document.getElementById("continue-button");
  if (continueButton) {
    continueButton.addEventListener("click", function (event) {
      event.preventDefault();
      createOrder();
    });
  }
});
