using UnityEngine;
using WebSocketSharp;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System;

[System.Serializable]
public class VehicleData
{
    public string id;
    public float x;
    public float y;
    public float heading;
}

public class WebSocketClient : MonoBehaviour
{
    CarSpawner carSpawner;
    WebSocket ws;

    public GameObject playerPrefab;    

    private readonly ConcurrentQueue<Action> _actions = new ConcurrentQueue<Action>();

    private void Start()
    {   
        
        carSpawner = GameObject.FindGameObjectWithTag("CarSpawner").GetComponent<CarSpawner>();

        ws = new WebSocket("ws://localhost:1123");
        ws.OnMessage += (sender, e) => {
            // Debug.Log(e.Data);

            Dictionary<string, object> jsonDict = JsonConvert.DeserializeObject<Dictionary<string, object>>(e.Data);

            string action_json = jsonDict["action"].ToString();

            switch (action_json){
                case "add_vehicle":
                    var dataObject = jsonDict["data"];
                    var vehicleData = JsonConvert.DeserializeObject<VehicleData>(dataObject.ToString());
                    string vehicleId = vehicleData.id;

                    // Debug.Log(vehicleId);
                    _actions.Enqueue(() => carSpawner.GenerateVehicle(vehicleId));
                    break;
                case "update_vehicles":
                    List<VehicleData> dataList = JsonConvert.DeserializeObject<List<VehicleData>>(jsonDict["data"].ToString());

                    foreach (VehicleData data in dataList){
                        // Debug.Log("ID: " + data.id + ", X: " + data.x + ", Y: " + data.y);
                        _actions.Enqueue(() => carSpawner.updateVehicle(data.id, data.x, data.y, data.heading));
                    }

                    break;
                default:
                    Debug.LogError("Unknown action: " + action_json);
                    break;
            }
        };
        ws.Connect();
    }

    private void Update ()
    {
        // Work the dispatched actions on the Unity main thread
        while(_actions.Count > 0)
        {
            if(_actions.TryDequeue(out var action))
            {
                action?.Invoke();
            }
        }
    }
}