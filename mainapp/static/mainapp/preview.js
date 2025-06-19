function displayPreview(elementId, model_id, revision, options) {
	var url = "/api/model/" + model_id + "/" + revision;

	window.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('renderCanvas');

    var engine = new BABYLON.Engine(canvas, true);

    var createScene = function () {
        var scene = new BABYLON.Scene(engine);
        scene.environmentTexture = BABYLON.CubeTexture.CreateFromPrefilteredData("https://playground.babylonjs.com/textures/environment.env", scene);

        var camera = new BABYLON.ArcRotateCamera("camera", -Math.PI / 2, Math.PI / 2.5, 3, BABYLON.Vector3.Zero(), scene);
        camera.attachControl(canvas, true);

        var light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(1, 1, 0), scene);

        BABYLON.SceneLoader.Append(url, "", scene, function () {
            scene.createDefaultEnvironment();
        });

        return scene;
    };

    var scene = createScene();
    engine.runRenderLoop(function () {
        scene.render();
    });

    window.addEventListener("resize", function () {
        engine.resize();
    });
});

}

function setupRenderPanes() {
	var elems = document.querySelectorAll('div.render-pane');

	for(var elem of elems) {
		var properties = elem.id.match(/render-pane(\d+).(\d+)/);
		displayPreview(elem.id, properties[1], properties[2]);
	}
}

setupRenderPanes();
