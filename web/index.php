<?php
$mysqli = new mysqli("db", "root", "root", "comparateur_db");

$sql = "SELECT 
            a.title, 
            MIN(s.price) as p1, 
            MIN(a.price) as p2, 
            MAX(s.url) as u1, 
            MAX(a.url) as u2
        FROM articles a
        JOIN articles s ON s.title = a.title
        WHERE s.source = 'Sodishop' 
        AND a.source = 'Apple Shop'
        GROUP BY a.title";

$result = $mysqli->query($sql);
?>
<!DOCTYPE html>
<html>
<body>
    <table border="1">
        <tr>
            <th>Produit</th>
            <th>Sodishop</th>
            <th>Apple Shop</th>
            <th>Verdict</th>
        </tr>
        <?php while($row = $result->fetch_assoc()): ?>
        <tr>
            <td><?php echo $row['title']; ?></td>
            <td><a href="<?php echo $row['u1']; ?>"><?php echo $row['p1']; ?> CFA</a></td>
            <td><a href="<?php echo $row['u2']; ?>"><?php echo $row['p2']; ?> CFA</a></td>
            <td><?php echo ($row['p1'] < $row['p2']) ? "Sodishop est moins cher" : "Apple Shop est moins cher"; ?></td>
        </tr>
        <?php endwhile; ?>
    </table>
</body>
</html>