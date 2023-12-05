// Mostrar el mensaje de contacto
//alert('¡Tu mensaje fue enviado correctamente!');

import Swal from 'sweetalert2/dist/sweetalert2.js'
import 'sweetalert2/src/sweetalert2.scss'

function mensaje(){
    Swal.fire({
        title: 'Error!',
        text: '¡Tu mensaje fue enviado correctamente!',
        icon: 'error',
        confirmButtonText: 'Cool'
      })          
}
