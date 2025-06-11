-- CREATE DATABASE punto_venta_django

SELECT @@max_allowed_packet;

 SELECT @@max_allowed_packet / 1024 / 1024;
 
 
 -- SET GLOBAL net_buffer_length=1000000;
 
 
-- SET GLOBAL max_allowed_packet=1073741824;

-- ALTER TABLE loggin_usuarios AUTO_INCREMENT=1;

-- ALTER TABLE loggin_sesiones AUTO_INCREMENT=1;

-- ALTER TABLE loggin_restablecer_contras AUTO_INCREMENT=1;

-- ALTER TABLE loggin_historial_sesiones AUTO_INCREMENT=0;

-- ALTER TABLE administrador_codigos AUTO_INCREMENT=0;



-- ALTER TABLE productos_productos AUTO_INCREMENT=0;

-- ALTER TABLE productos_galeria_prod AUTO_INCREMENT=0;`punto_venta_django`

-- ALTER TABLE productos_detalle_prod AUTO_INCREMENT=0;

-- ALTER TABLE productos_seccion_prod AUTO_INCREMENT=4;

-- ALTER TABLE productos_color AUTO_INCREMENT=0;

-- ALTER TABLE productos_detalle_prod AUTO_INCREMENT=0;

-- ALTER TABLE productos_inventario AUTO_INCREMENT=0;



select 	`id`, 
`created`, 
`modified`, 
`d_codigo`, 
`d_asenta`, 
`D_mnpio`, 
`d_ciudad`, 
`c_estado`, 
`c_oficina`, 
`c_tipo_asenta`, 
`c_mnpio`, 
`id_asenta_cpcons`, 
`d_zona`, 
`c_cve_ciudad`, 
`d_CP`

from 
`punto_venta_django`.`django_postalcodes_mexico_postalcode` 
-- where d_codigo = 50850


	
select * FROM loggin_restablecer_contras where fk_sesion_id=1 or activa = 'SI' or bandera=1



select * 
from loggin_usuarios as u
inner join loggin_municipios as m on m.id_municipios = u.fk_municipios
inner join loggin_estados as e on e.id_estados = m.fk_estados_id
inner join loggin_pais as p on p.id_pais = e.fk_pais_id
where u.id_usuarios = 2



select * from administrador_codigos where activo = 5 or activo= 0 order by id_codigo limit 1


-- consulta del detalle productos
select * 
from productos_detalle_prod as dp
inner join productos_productos as p on p.id_producto = dp.fk_productos_id
inner join productos_seccion_prod as s on s.id_seccion = dp.fk_seccion_id
inner join productos_tipo_producto as t on t.id_tipo_prod = dp.fk_tipo_id
where p.uuid_producto = '0902d820-ab9d-45b3-810d-f105bb3b3d6f'
and t.talla = 20



SELECT * 
FROM productos_detalle_prod AS dp
INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
INNER JOIN productos_seccion AS s ON s.id_seccion = dp.fk_seccion_id
INNER JOIN productos_tipo_producto AS t ON t.id_tipo_prod = dp.fk_tipo_id
WHERE p.uuid_producto = '0902d820-ab9d-45b3-810d-f105bb3b3d6f'



SELECT * 
FROM productos_detalle_prod AS dp
INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
INNER JOIN productos_seccion_prod AS s ON s.id_seccion = dp.fk_seccion_id
INNER JOIN productos_tipo_producto AS t ON t.id_tipo_prod = dp.fk_tipo_id
group by dp.fk_productos_id
order by dp.fk_productos_id




SELECT * 
FROM productos_detalle_prod AS dp 
INNER JOIN productos_productos as p on p.id_producto = dp.fk_productos_id
inner join productos_color as c on c.id_color = dp.fk_color_id
inner join productos_tallas as t on t.id_tallas = dp.fk_talla_id
inner join productos_tipo as tp on tp.id_tipo = dp.fk_tipo_id
inner join productos_seccion as s on s.id_seccion = dp.fk_seccion_id
WHERE p.uuid_producto = 'c751884a-0351-49f2-98dc-fa52fef14def'
group by c.color


SELECT * 
FROM productos_detalle_prod AS dp 
INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
WHERE p.uuid_producto = '336aa6ee-835d-48ca-9fcd-9e58b443fb7a'
and dp.fk_color_id = 2
and dp.fk_tipo_id = 1 
and dp.fk_seccion_id = 1


select * from productos_detalle_prod where fk_color_id = 1 and fk_productos_id = 1 and fk_tipo_id = 1 and fk_seccion_id = 1





SELECT * 
FROM productos_detalle_prod AS dp 
INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
INNER JOIN productos_color AS c ON c.id_color = dp.fk_color_id
INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
INNER JOIN productos_tipo AS tp ON tp.id_tipo = dp.fk_tipo_id
INNER JOIN productos_seccion AS s ON s.id_seccion = dp.fk_seccion_id
WHERE p.id_producto = 1
AND c.id_color = 2


SELECT * 
FROM productos_detalle_prod AS dp 
INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
INNER JOIN productos_color AS c ON c.id_color = dp.fk_color_id
INNER JOIN productos_tipo AS tp ON tp.id_tipo = dp.fk_tipo_id
INNER JOIN productos_seccion AS s ON s.id_seccion = dp.fk_seccion_id
WHERE p.id_producto = 1
GROUP BY c.color


select * 
from productos_inventario as inv 
inner join productos_detalle_prod AS dp on dp.id_detalle = inv.fk_det_productos_id
INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
INNER JOIN productos_color AS c ON c.id_color = dp.fk_color_id
INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
INNER JOIN productos_tipo AS tp ON tp.id_tipo = dp.fk_tipo_id
INNER JOIN productos_seccion AS s ON s.id_seccion = dp.fk_seccion_id
WHERE p.id_producto = 1
GROUP BY c.color



SELECT * 
FROM productos_inventario AS inv 
INNER JOIN productos_detalle_prod AS dp ON dp.id_detalle = inv.fk_det_productos_id
INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
INNER JOIN productos_color AS c ON c.id_color = dp.fk_color_id
INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
INNER JOIN productos_tipo AS tp ON tp.id_tipo = dp.fk_tipo_id
INNER JOIN productos_seccion AS s ON s.id_seccion = dp.fk_seccion_id
WHERE p.id_producto = 1



select *
from productos_productos as p
inner join productos_galeria_prod as g on g.fk_productos_id = p.id_producto
group by p.codigo
order by p.id_producto


SELECT *, sum(stock) as total_stock, 
case WHEN SUM(stock) = '' or sum(stock) = 0 or sum(stock) = (null) THEN "#ffffff;" 
when sum(stock) < 50 then "#f8a1a1;" 
when sum(stock) < 500 then "#fff69b;" 
WHEN SUM(stock) > 500 THEN "#b8ff9b;" 
end as cod_color
FROM productos_inventario AS inv
INNER JOIN productos_detalle_prod AS dp ON dp.id_detalle = inv.fk_det_productos_id
right JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
group by p.id_producto




SELECT * 
FROM productos_detalle_prod AS dp 
RIGHT JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
INNER JOIN productos_color AS c ON c.id_color = dp.fk_color_id
INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
INNER JOIN productos_tipo AS tp ON tp.id_tipo = dp.fk_tipo_id
INNER JOIN productos_seccion AS s ON s.id_seccion = dp.fk_seccion_id
WHERE p.id_producto = 4
AND c.id_color = 6




-- para el detalle de compra de producto
SELECT * 
FROM productos_detalle_prod AS dp 
INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
INNER JOIN productos_tipo AS tp ON tp.id_tipo = dp.fk_tipo_id
INNER JOIN productos_seccion AS s ON s.id_seccion = dp.fk_seccion_id
WHERE p.id_producto = 1
group by p.id_producto



SELECT * 
FROM productos_inventario AS inv 
INNER JOIN productos_detalle_prod AS dp ON dp.id_detalle = inv.fk_det_productos_id
INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
INNER JOIN productos_color AS c ON c.id_color = dp.fk_color_id
INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
INNER JOIN productos_tipo AS tp ON tp.id_tipo = dp.fk_tipo_id
INNER JOIN productos_seccion AS s ON s.id_seccion = dp.fk_seccion_id
WHERE p.id_producto = 1



SELECT * , count(fk_color_id)
FROM productos_detalle_prod AS dp 
WHERE dp.fk_productos_id = 1
group by dp.fk_color_id

