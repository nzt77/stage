function result(){
    let name = document.getElementById('name').ariaValueMax;
    let surname = document.getElementById('surname').ariaValueMax;
    sessionStorage.setItem('Nom',name);
    sessionStorage.setItem('Prenom',surname);
}
