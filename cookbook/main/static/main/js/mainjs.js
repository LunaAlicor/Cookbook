function updateCurrentTime() {
    const currentTimeElement = document.getElementById("current-time");
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    const currentTimeString = `${hours}:${minutes}:${seconds}`;
    currentTimeElement.textContent = currentTimeString;
}

setInterval(updateCurrentTime, 1000);
updateCurrentTime();



const themeToggle = document.getElementById("theme-toggle");
const body = document.body;
const dropdown = document.getElementById("dropdown");
var sidelist = document.getElementById('sidelist');
var dropdownbutton = document.getElementById('dropdownbutton');
const cartElements = document.querySelectorAll(".card-header");
const cardBodyElements = document.querySelectorAll(".card-body");

function setThemeStatus(status) {
  if (status) {
    body.classList.add("dark-theme");
    dropdown.style.backgroundColor = "#fff";
    sidelist.style.background = '#fff';
    dropdownbutton.style.background = '#fff';

    cartElements.forEach(element => {
      element.style.background = "#333333";
    });

    cardBodyElements.forEach(element => {
      element.style.background = "#333333";
    });

  } else {
    body.classList.remove("dark-theme");
    dropdown.style.backgroundColor = "#333333";
    sidelist.style.background = '#333333';
    dropdownbutton.style.background = '#333333';

    cartElements.forEach(element => {
      element.style.background = "#fff";
    });

    cardBodyElements.forEach(element => {
      element.style.background = "#fff";
    });
  }
}

const storedThemeStatus = localStorage.getItem("themeStatus");

if (storedThemeStatus === "1") {
  themeToggle.checked = true;
  setThemeStatus(true);
} else {
  themeToggle.checked = false;
  setThemeStatus(false);
}

themeToggle.addEventListener("change", () => {
  if (themeToggle.checked) {
    setThemeStatus(true);
    localStorage.setItem("themeStatus", "1");
  } else {
    setThemeStatus(false);
    localStorage.setItem("themeStatus", "0");
  }
});


document.getElementById("toggleSidebar").addEventListener("click", function() {
  var sidebar = document.getElementById("sidebar");
  var firstsidebarbutton = document.getElementById('toggleSidebar');
  var firstsidebarbutton2 = document.getElementById('toggleSidebar2');

function openSidebar() {

  // const storedThemeStatus = localStorage.getItem("themeStatus");
  sidebar.style.left = "0";
  sidebar.style.display = 'block';
  firstsidebarbutton.style.display = "none";
  // if (storedThemeStatus === '0'){
  //   sidelist.style.background = '#fff';
  // } else {
  //   sidelist.style.background = '#333333';
  // }
}


var toggleSidebarButton = document.getElementById('toggleSidebar');
toggleSidebarButton.addEventListener('click', openSidebar);


  function resetSidebar() {

    sidebar.style.left = "-250px";
    sidebar.style.display = 'none';
    firstsidebarbutton.style.display = "block";
  }

  firstsidebarbutton2.addEventListener('click', resetSidebar);
});


document.getElementById('update-prices-btn').addEventListener('click', function() {
    fetch('/update_prices/')
        .then(response => response.json())
        .then(data => {

            console.log(data);
        })
        .catch(error => {
            console.error('Произошла ошибка:', error);
        });
});


document.getElementById('update-prices-btn2').addEventListener('click', function() {
    fetch('/update_prices2/')
        .then(response => response.json())
        .then(data => {

            console.log(data);
        })
        .catch(error => {
            console.error('Произошла ошибка:', error);
        });
});


$(document).ready(function() {
    $('#product-search').on('input', function() {
        var query = $(this).val();
        if (query) {
            $.get('/search_product/', {q: query}, function(data) {
                var results = data.results;
                var resultHtml = '<ul>';
                for (var i = 0; i < results.length; i++) {
                    resultHtml += '<li data-id="' + results[i].id + '">' + results[i].name + '</li>';
                }
                resultHtml += '</ul>';
                $('#search-results').html(resultHtml);


                $('#search-results li').on('click', function() {
                    var productId = $(this).data('id');
                    var productName = $(this).text();
                    $('#product-search').val(productName);

                });
            });
        } else {
            $('#search-results').html('');
        }
    });
});

function decreaseQuantity(productId) {
    console.log('Start decreaseQuantity');
    $.ajax({
        url: `/decrease_quantity/${productId}/`,
        type: 'POST',
        success: function(data) {
            console.log('Success:', data);
            $('#quantity_' + productId).text(data.quantity);
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}

function deleteProduct(productId) {

    $.ajax({
        url: `/delete_product/${productId}/`,
        type: 'POST',
        success: function() {

            $('#quantity_' + productId).closest('.custom-item').remove();
        },
        error: function(error) {
            console.log(error);
        }
    });
}


function increaseQuantity(productId) {
    console.log('Start decreaseQuantity');
    $.ajax({
        url: `/increase_quantity/${productId}/`,
        type: 'POST',
        success: function(data) {
            console.log('Success:', data);
            $('#quantity_' + productId).text(data.quantity);
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}

function searchProducts() {
    const query = document.getElementById('productInput').value;
    if (query.trim() !== '') {
        fetch(`/api/products/?name=${query}`)
            .then(response => response.json())
            .then(data => {
                displayProducts(data);
            })
            .catch(error => {
                console.error('Ошибка при поиске продуктов:', error);
            });
    }
}

function displayProducts(products) {
    const productList = document.getElementById('productList');
    productList.innerHTML = '';

    products.forEach(product => {
        const listItem = document.createElement('li');
        listItem.textContent = product.name;

        const addButton = document.createElement('button');
        addButton.textContent = 'Добавить в рецепт';
        addButton.onclick = function() {
            addProductToRecipe(product.id, product.name);
        };

        listItem.appendChild(addButton);
        productList.appendChild(listItem);
    });
}

function addProductToRecipe(productId, productName) {
    // Логика добавления выбранного продукта к рецепту через API
    // Напишите эту функцию в соответствии с вашими запросами к API
    // Например, используя fetch или другой метод

    // Пример:
    fetch(`/api/recipes/${recipeId}/add_product/?product_id=${productId}`, {
        method: 'POST',
        // Добавьте другие параметры запроса при необходимости
    })
    .then(response => {
        // Обработка успешного добавления продукта к рецепту
        console.log('Продукт успешно добавлен к рецепту:', productName);
    })
    .catch(error => {
        console.error('Ошибка при добавлении продукта к рецепту:', error);
    });
}