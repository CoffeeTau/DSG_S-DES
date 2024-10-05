document.getElementById('submitButton').addEventListener('click', function() {
    const inputField = document.getElementById('myInput');
    const inputValue = inputField.value;
    document.getElementById('output').innerText = `你输入的内容是：${inputValue}`;
});