const cargarProductos = async (idCategoria, idSubcategoria) => {
    try {
        const response = await fetch(`./producto/${idCategoria}/${idSubcategoria}`);
        const data = await response.json();
        
        if (data.message=="Éxito"){
            const productosContainer = document.getElementById('productos-container');
            productosContainer.innerHTML = '';  // Limpiar contenido existente
            data.productos.forEach(producto => {
                const productoHTML = `
                    <div class="col-2 mt-3 mb-3 text-center">
                        <a href="#" style="text-decoration:none;">
                            <div class="card">
                                <div class="card-header">${producto.nombre}</div>
                                <div class="card-body">
                                    <img
                                        src="${producto.foto}"
                                        alt="Foto de ${producto.nombre}"
                                        width="150"
                                        height="100"
                                    />
                                    <hr />
                                    <span>$${producto.precio}</span>
                                    <hr />
                                    <span>Cantidad: ${producto.cantidad}</span>
                                    <hr />
                                    <button class="btn btn-outline-dark" type="#" style="text-transform:capfirst;">Agregar al carrito</button>
                                </div>
                            </div>
                        </a>
                    </div>
                `;
                productosContainer.innerHTML += productoHTML;
            });
        } else {
            console.error('No se obtuvieron productos');
            const productosContainer = document.getElementById('productos-container');
            productosContainer.innerHTML = 'No existen productos.';
        }
    } catch (error) {
            console.error('Error al cargar productos:', error);
    }
};

const listarSubcategorias = async (idCategoria) => {
    try {
        const response = await fetch(`./subcategorias/${idCategoria}`);
        const data = await response.json();
        
        if (data.message=="Éxito"){
            let opciones = ``;
            data.subcategoria.forEach((subcategoria) =>{
                opciones += `<option value='${subcategoria.id}'>${subcategoria.nombre}</option>`;
            })
            cboSubcategoria.innerHTML = opciones;
            cargarProductos(idCategoria, data.subcategoria[0].id);    
        } else {
            alert("Subcategorías no encontradas")
        }
    } catch (error) {
        console.error("Error al cargar subcategorías:", error);
        // Puedes mostrar un mensaje de error al usuario o realizar otras acciones apropiadas.
    }
};

const listarCategorias = async () => {
    try {
        const response = await fetch("./categorias");
        const data = await response.json();
        
        if (data.message=="Éxito"){
            let opciones = ``;
            data.categoria.forEach((categoria) =>{
                opciones += `<option value='${categoria.id}'>${categoria.nombre}</option>`;
            })
            cboCategoria.innerHTML = opciones;
            listarSubcategorias(data.categoria[0].id);

        } else {
            alert("Categorías no encontradas")
        }
    } catch (error) {
        console.error("Error al cargar categorías:", error);
        // Puedes mostrar un mensaje de error al usuario o realizar otras acciones apropiadas.
    }
};

const cargaInicial = async () => {
    await listarCategorias();

    cboCategoria.addEventListener("change", async (evento) => {
        const idCategoriaSeleccionada = evento.target.value;
        
        // Llamar a listarSubcategorias y guardar el resultado
        const subcategoriasResponse = await listarSubcategorias(idCategoriaSeleccionada);

        // Verificar si listarSubcategorias fue exitoso antes de llamar a cargarProductos
        if (subcategoriasResponse && subcategoriasResponse.message === "Éxito") {
            cargarProductos(idCategoriaSeleccionada, subcategoriasResponse.subcategoria[0].id);
        } else {
            console.error("No se pudieron cargar las subcategorías");
        }
    });

    cboSubcategoria.addEventListener("change", (evento) => {
        const idCategoriaSeleccionada = cboCategoria.value; // Obtener la categoría actualmente seleccionada
        const idSubcategoriaSeleccionada = evento.target.value; // Obtener la subcategoría seleccionada

        cargarProductos(idCategoriaSeleccionada, idSubcategoriaSeleccionada);
    });
};

/*
const cargaInicial = async () => {
    await listarCategorias();

    cboCategoria.addEventListener("change", (evento) => {
        //console.log(evento);
        //console.log(evento.target);
        //console.log(evento.target.value);
        listarSubcategorias(evento.target.value);
        cargarProductos(evento.target.value, listarSubcategorias(evento.target.value));
    })

    cboSubcategoria.addEventListener("change", (evento) => {
        //console.log(evento);
        //console.log(evento.target);
        //console.log(evento.target.value);
        cargarProductos(evento.target.value, evento.target.value);
    })
};
*/

window.addEventListener("load", async () => {
    await cargaInicial();
});