function pixel_cm(num_pixels) {
    return num_pixels * 0.0264;
}

function cm_pixel(cms) {
    return int(cms / 0.0264);
}

function cell_area(cellId) {
    let j = cell_coords[cellId].length - 1;
    let area = 0.0;

    for (let i = 0; i < cell_coords[cellId].length; ++i) {
        area += (cell_coords[cellId][j][0] + cell_coords[cellId][i][0]) *
            (cell_coords[cellId][j][1] - cell_coords[cellId][i][1]);
        j = i;

    }
    return area;
}