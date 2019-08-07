var points;
var nornal;
var BGCOLOUR = 51;
var img;

function preload() {
    img = loadImage('mars-viking-zoom.jpg');
}

function setup() {
    createCanvas(1000, 641);
    background(BGCOLOUR);
    noSmooth();


    image(img, 0, 0, 640, 640);

    //Set Site Stroke
    voronoiSiteStroke(BGCOLOUR);

    voronoiRndSites(60, 50);
    // Build Voronoi Diagram
    voronoi(640, 640, true);
    // voronoiDraw(0, 0, true, false);
    cell_coords = voronoiGetCells();
    console.log(cell_coords);

    // Draw Voronoi lines
    draw_voronoi();

}

function draw() {


}

function mouseClicked() {
    background(BGCOLOUR);
    var cellId = voronoiGetSite(mouseX, mouseY, false);
    draw_voronoi();

    console.log(cell_coords[cellId]);
    // Display the cell only when clicked inside the voronoi
    if (typeof cellId != 'undefined') {

        draw_cell(700, 50, cellId)
    }


}

function draw_cell(posx, posy, cellId, scale = 1.6) {

    let minX = Number.MAX_VALUE;
    let minY = Number.MAX_VALUE;
    for (let i = 0; i < cell_coords[cellId].length; i++) {
        if (cell_coords[cellId][i][0] < minX)
            minX = cell_coords[cellId][i][0];
        if (cell_coords[cellId][i][1] < minY)
            minY = cell_coords[cellId][i][1];
    }

    strokeWeight(3);
    stroke(237, 34, 93);
    noFill();
    beginShape();
    for (let j = 0; j < cell_coords[cellId].length; ++j) {

        let x1 = (cell_coords[cellId][j][0] - minX) * scale + posx;
        let y1 = (cell_coords[cellId][j][1] - minY) * scale + posy;
        vertex(x1, y1);
    }
    endShape(CLOSE);

    // Display the side lengths in cms
    let x2, y2, d;

    for (let j = 0; j < cell_coords[cellId].length; ++j) {

        let x1 = (cell_coords[cellId][j][0] - minX) * scale + posx;
        let y1 = (cell_coords[cellId][j][1] - minY) * scale + posy;

        if (j == cell_coords[cellId].length - 1) {
            x2 = (cell_coords[cellId][0][0] - minX) * scale + posx;
            y2 = (cell_coords[cellId][0][1] - minY) * scale + posy;


            d = pixel_cm(dist(cell_coords[cellId][j][0], cell_coords[cellId][j][1],
                cell_coords[cellId][0][0], cell_coords[cellId][0][1]));
        } else {
            x2 = (cell_coords[cellId][j + 1][0] - minX) * scale + posx;
            y2 = (cell_coords[cellId][j + 1][1] - minY) * scale + posy;

            d = pixel_cm(dist(cell_coords[cellId][j][0], cell_coords[cellId][j][1],
                cell_coords[cellId][j + 1][0], cell_coords[cellId][j + 1][1]));

        }

        push();
        translate((x1 + x2) / 2, (y1 + y2) / 2); // center the text
        let ang = atan2((y2 - y1), x2 - x1);

        // make sure the text is readable
        ang = (ang < -1.5 || ang > 2) ? 3.141 + ang : ang;
        rotate(ang);
        strokeWeight(0.8);
        stroke(255);
        text(nfc(d, 2) + " cm", -10, 15);
        pop();

    }

}

function draw_voronoi() {
    strokeWeight(3);
    stroke(237, 34, 93);
    noFill();

    for (let i = 0; i < cell_coords.length; ++i) {
        beginShape();
        for (let j = 0; j < cell_coords[i].length; ++j) {
            vertex(cell_coords[i][j][0], cell_coords[i][j][1]);
        }
        endShape(CLOSE);
    }
}