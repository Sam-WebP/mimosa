import { API } from "./api.js";
import { StateManager, stateKeys } from "./stateManager.js";

const htmlListCertificates = "#list-certificates";
const htmlListFees = "#list-fees";
const htmlOrderSummary = "#order-summary";
const htmlContinueButton = "#continue-button";

/**
 * Updates the order summary with the selected certificates and fees.
 */
function updateSummary() {
  let total = 0;
  const selectedCertificates = document.querySelectorAll(
    `${htmlListCertificates} input[type="checkbox"]:checked`
  );
  const selectedFees = document.querySelectorAll(
    `${htmlListFees} input[type="checkbox"]:checked`
  );

  selectedCertificates.forEach((item) => {
    const price = parseFloat(item.dataset.price);
    console.debug(`Selected certificate: ${item.value}, Price: ${price}`);
    total += price;
  });

  selectedFees.forEach((item) => {
    const price = parseFloat(item.dataset.price);
    console.debug(`Selected fee: ${item.name}, Price: ${price}`);
    total += price;
  });

  console.debug(`Total calculated: ${total}`);

  const summaryElement = document.querySelector(htmlOrderSummary);
  if (summaryElement) {
    summaryElement.textContent = `Total: ${total.toFixed(2)}`;
  }
}

/**
 * Creates an order session
 */
function createOrder() {
  const selectedCertificates = Array.from(
    document.querySelectorAll(
      `${htmlListCertificates} input[type="checkbox"]:checked`
    )
  ).map((checkbox) => ({
    certificate_id: parseInt(checkbox.value),
    fee_id: null,
  }));

  const selectedFees = Array.from(
    document.querySelectorAll(`${htmlListFees} input[type="checkbox"]:checked`)
  ).map((checkbox) => parseInt(checkbox.value));

  /**
   * Assign fee_id to each certificate if available
   */
  for (let i = 0; i < selectedCertificates.length; i++) {
    if (i < selectedFees.length) {
      selectedCertificates[i].fee_id = selectedFees[i];
    }
  }

  const selectedProperty = StateManager.getState(stateKeys.selectedProperty);
  const propertyId = selectedProperty ? selectedProperty.id : null;

  const data = {
    property_id: propertyId,
    lines: selectedCertificates,
  };

  console.debug("Data being sent to server:", data);

  /**
   * Create the order session
   */
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
    `${htmlListCertificates} input[type="checkbox"], ${htmlListFees} input[type="checkbox"]`
  );
  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", updateSummary);
  });

  updateSummary();

  const continueButton = document.querySelector(htmlContinueButton);
  if (continueButton) {
    continueButton.addEventListener("click", function (event) {
      event.preventDefault();
      createOrder();
    });
  }
});
