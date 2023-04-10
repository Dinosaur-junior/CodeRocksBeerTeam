function Complete() {
    var int = document.SimpleIntForm.int.value;
    document.getElementById("result").innerHTML = '<div class="alert alert-info" role="alert">'+int + ' - ' + isPrime(int) + '</div>';
    }

function isPrime(n) {
  if (n < 2) {
    return 'Число должно быть больше 1';
  } else if (n === 2) {
    return 'Простое число';
  }

  let i = 2;
  const limit = Math.sqrt(n);
  while (i <= limit) {
    if (n % i === 0) {
      return 'Составное число';
    }
    i +=1;
  }

  return 'Простое число';
}