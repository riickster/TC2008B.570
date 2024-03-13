using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

[System.Serializable]
public class Vehicle
{
    public string id;
    public float x;
    public float z;

    public Vehicle(string p_id, float p_x, float p_z){
        id = p_id;
        x = p_x;
        z = p_z;
    }

    public void update_X(float n_x){
        x = n_x; 
    }
    public void update_Z(float n_z){
        z = n_z; 
    }
}

public class CarSpawner : MonoBehaviour
{
    public List<Vehicle> vehicle_list = new List<Vehicle>();
    // public GameObject vehiclePrefab;

    public List<GameObject> prefabs;

    public void GenerateVehicle(string id){
        vehicle_list.Add(new Vehicle(id, -1000, -1000));
        var car = Instantiate(prefabs[Random.Range(0, 4)], new Vector3(-1000, 0, -1000), Quaternion.identity);
        car.name = id;
    }

    public void DeleteVehicle(string vehicle_id){
        GameObject car = GameObject.Find(vehicle_id);
        Destroy(car);
    }

    public void updateVehicle(string vehicle_id, float n_x, float n_z, float heading){
        if(vehicle_list.Count != 0){
            GameObject car = GameObject.Find(vehicle_id);
            Vehicle vehicle_obj = vehicle_list.FirstOrDefault(i => i.id == vehicle_id);

            if(vehicle_obj != null){
                vehicle_obj.update_X(n_x);
                vehicle_obj.update_Z(-n_z);
                car.transform.position = new Vector3(vehicle_obj.x, 0, vehicle_obj.z);
                car.transform.rotation = Quaternion.Euler(0, heading+90, 0);
            }
        }
    }
}
