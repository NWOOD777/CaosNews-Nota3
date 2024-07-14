function EliminarPeri(id){
    Swal.fire({
        title: "¿Seguro que desea eliminar "+id+"?",
        text: "",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonText: "CANCELAR",
        cancelButtonColor: "#d33",
        confirmButtonText: "ELIMINAR"
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire({
            title: "ELIMINADO!",
            text: "El periodista ha sido eliminado",
            icon: "success"
          }).then(function(){
            window.location.href = "/periodistas/delete/"+id+"/";
          });
        }
      });
}

function confiEliminarN(id){
  Swal.fire({
      title: "¿Seguro que desea eliminar "+id+"?",
      text: "",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonText: "CANCELAR",
      cancelButtonColor: "#d33",
      confirmButtonText: "ELIMINAR"
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "ELIMINADO!",
          text: "La noticia ha sido eliminado",
          icon: "success"
        }).then(function(){
          window.location.href = "/noticias/delete/"+id+"/";
        });
      }
    });
}