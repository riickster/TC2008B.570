using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrafficLightController : MonoBehaviour
{
    public int cycle = 0;

    public void UpdateLightCycle(){

        if(cycle == 0){
            TurnLight("Series_1_Red", false);
            TurnLight("Series_1_Green", true);

            TurnLight("Series_2_Red", true);
            TurnLight("Series_2_Green", false);

            cycle = 1;
        } else {
            TurnLight("Series_1_Red", true);
            TurnLight("Series_1_Green", false);

            TurnLight("Series_2_Red", false);
            TurnLight("Series_2_Green", true);

            cycle = 0;
        }
        
    }

    void TurnLight(string tag, bool status){
        GameObject[] taggedLights = GameObject.FindGameObjectsWithTag(tag);
        foreach (GameObject lightObject in taggedLights)
        {
            Light lightComponent = lightObject.GetComponent<Light>();
            if (lightComponent != null){
                lightComponent.enabled = status;
            }
        }
    }
}
