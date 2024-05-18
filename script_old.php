<?php

CModule::IncludeModule('iblock');

use Bitrix\Main\Web\HttpClient;

function parseJsonFromUrl($url) {
	$httpClient = new HttpClient();
	$response = $httpClient->get($url);

	if ($response === FALSE) {
		die('Error occurred');
	}

    $dataArray = json_decode($response, true);

    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("JSON decode error: " . json_last_error_msg());
    }

    foreach ($dataArray as $dataObject) {        
        $el = new CIBlockElement;
        $PROP = array();
        if ($dataObject['Телефон'] !== null) {
            $PROP[1] = $dataObject['Телефон'];
        }
        if ($dataObject['Почта'] !== null) {
            $PROP[241] = $dataObject['Почта'];
        }
        if ($dataObject['Сумма'] !== null) {
            $PROP[4] = $dataObject['Сумма'];
        } else {
            $PROP[4] = 0;
        }
        if ($dataObject['Тип'] !== null) {
            $PROP[8] = $dataObject['Тип'];
        }
        if ($dataObject['ФИО'] === null) {
            $name = $dataObject['Плательщик'];
        } else {
			$name = $dataObject['ФИО'];
		}

        $patientID = null;
        $b24ID = null;
        foreach ($dataObject['Пациент'] as $patient) {
            $patientFilter = [
				"IBLOCK_ID" => 56, 
				"%NAME" => $patient
			];
            $patientRes = CIBlockElement::GetList([], $patientFilter, false, false, ["ID", "PROPERTY_B24_ID"]);
            if ($patientObj = $patientRes->Fetch()) {
                $patientID = $patientObj['ID'];
                $b24ID = $patientObj['PROPERTY_B24_ID_VALUE'];
                break;
            }
        }

        if ($patientID !== null) {
            $fundraiserFilter = ["IBLOCK_ID" => 57, "ACTIVE" => "Y", "PROPERTY_PATIENT" => $patientID];
            $fundraiserRes = CIBlockElement::GetList([], $fundraiserFilter, false, false, ["ID", "NAME", "PROPERTY_TARGET", "PROPERTY_B24_ID"]);
            if ($fundraiserObj = $fundraiserRes->Fetch()) {
                $PROP[10] = 'FBL' . mb_substr($fundraiserObj['PROPERTY_B24_ID_VALUE'], -4);
                $PROP[236] = $fundraiserObj['PROPERTY_B24_ID_VALUE'];
                $PROP[238] = $b24ID;
            }
        }

        $arLoadProductArray = Array(
            "MODIFIED_BY"    => 7, // $USER->GetID(),
            "IBLOCK_SECTION_ID" => false,
            "IBLOCK_ID"      => 4,
            "PROPERTY_VALUES"=> $PROP,
            "NAME"           => $name,
            "ACTIVE"         => "Y",
        );
        if($PRODUCT_ID = $el->Add($arLoadProductArray)) {
            echo "New ID: ".$PRODUCT_ID;
        } else {
            echo "Error: ".$el->LAST_ERROR;
        }
    }
}

?>
