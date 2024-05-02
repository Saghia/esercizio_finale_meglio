const verificaPrenotazione = document.getElementById("verificaPrenotazione");
const confermaPrenotazione = document.getElementById("confermaPrenotazione");
const orarioPrenotazione = document.getElementById("orarioPrenotazione");
const dataPrenotazione = document.getElementById("dataPrenotazione");
const numeroClienti = document.getElementById("numeroClienti");
const verificaButton = document.getElementById("verificaButton");
const confermaButton = document.getElementById("confermaButton");

let disponibile = false;

const endpoint = "http://localhost:8000/";

verificaButton.addEventListener("click", verificaDisponibilita);
confermaButton.addEventListener("click", conferma);

const verificaDisponibilita = async () => {
  if (orarioPrenotazione == 0 || dataPrenotazione == null) return;
  const path = "api/check_tavolo";
  const response = await fetch(endpoint + path, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify({
      ora: orarioPrenotazione.value,
      data: dataPrenotazione.value,
    }),
  });
  if (response.status == 200) {
    disponibile = true;
    const responseJSON = response.json();
    console.log(responseJSON);
    verificaPrenotazione.classList.add("d-none");
    confermaPrenotazione.classList.remove("d-none");
  } else {
    alert("TAVOLO GIA' PRENOTATO PER QUEST'ORA");
  }
};

async function conferma() {
  if (!disponibile) return;
  const path = "api/prenota";
  const response = await fetch(endpoint + path, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify({
      ora: orarioPrenotazione.value,
      data: dataPrenotazione.value,
      numero_persone: numeroClienti.value,
    }),
  });
  if (response.status == 201) {
    alert("TAVOLO PRENOTATO");
    window.location.reload();
  }
}
