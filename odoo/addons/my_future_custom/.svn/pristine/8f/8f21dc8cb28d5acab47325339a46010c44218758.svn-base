    (function () {

        $(document).ready(function(){
            // $(document).on ("change", "#rajaongkir_city_acc", function () {
            //     var subdistrict_val = this.value;
            //     var xmlhttp = new XMLHttpRequest();
            //     xmlhttp.onreadystatechange = function() {
            //         if (this.readyState == 4 && this.status == 200) {
            //             console.log("check_data", this)
            //             var data = JSON.parse(this.responseText);
            //             if(data){
            //                 var options = '<option disabled>Choose Subdistrict...</option>';
            //                 for(var i = 0 ; i < data.length; i++){
            //                     var selected = data[i].selected == 1 ? 'selected="1"' : '';
            //                     options += '<option value="'+data[i].id+'" '+selected+'>'+data[i].name+'</option>';
            //                 }
            //                 document.getElementById('rajaongkir_district_acc').innerHTML = options;
            //                 const districtSelect = document.getElementById('rajaongkir_district_acc');
            //                 console.log(options)
            //                 data.result.forEach(district => {
            //                     const option = document.createElement('option');
            //                     option.value = district.id;
            //                     option.text = district.name;
            //                     districtSelect.add(option);
            //                 });
            //             }
            //         }
            //     };
            
            //     xmlhttp.open("POST", "/portal/ajax/rajaongkir_district_acc", true);
            //     xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            //     xmlhttp.send(JSON.stringify({'rajaongkir_city_acc': subdistrict_val}));
            // });
            $(document).on ("change", "#myfuture_provinsi", function () {
                var id_provinsi = this.value;
                var xmlhttp = new XMLHttpRequest();
                xmlhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        var data = JSON.parse(this.responseText);
                        if(data){
                            var options = '<option>Pilih Kota...</option>';
                            for(var i = 0 ; i < data.length; i++){
                                var selected = data[i].selected == 1 ? 'selected="1"' : '';
                                options += '<option value="'+data[i].id+'" '+selected+'>'+data[i].name+'</option>';
                            }
                            document.getElementById('myfuture_kota').innerHTML = options;
                            const citySelect = document.getElementById('myfuture_kota');
                            console.log(options)
                            data.result.forEach(city => {
                                const option = document.createElement('option');
                                option.value = city.id;
                                option.text = city.name;
                                citySelect.add(option);
                            });
                        }
                    }
                };
            
                xmlhttp.open("POST", "/myfuture/get_city", true);
                xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                xmlhttp.send(JSON.stringify({'id_provinsi': id_provinsi}));
            });

            $(document).on ("change", "#myfuture_kota", function () {
                var id_kota = this.value;
                var xmlhttp = new XMLHttpRequest();
                xmlhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        var data = JSON.parse(this.responseText);
                        if(data){
                            var options = '<option>Pilih Kecamatan...</option>';
                            for(var i = 0 ; i < data.length; i++){
                                var selected = data[i].selected == 1 ? 'selected="1"' : '';
                                options += '<option value="'+data[i].id+'" '+selected+'>'+data[i].name+'</option>';
                            }
                            document.getElementById('myfuture_kecamatan').innerHTML = options;
                            const districtSelect = document.getElementById('myfuture_kecamatan');
                            console.log(options)
                            data.result.forEach(district => {
                                const option = document.createElement('option');
                                option.value = district.id;
                                option.text = district.name;
                                districtSelect.add(option);
                            });
                        }
                    }
                };
            
                xmlhttp.open("POST", "/myfuture/get_district", true);
                xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                xmlhttp.send(JSON.stringify({'id_kota': id_kota}));
            });
        })
    })();

